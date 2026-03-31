"""
Convert Markdown CVs to PDF using reportlab + DejaVu Sans (Unicode icons).

Usage:
  uv run --with reportlab md_to_pdf.py <folder> [--skip-sections Idiomas,Resumen]

Options:
  --skip-sections  Comma-separated list of H2 section titles to drop (e.g. Idiomas,Resumen)
  --no-border      Disable the decorative indigo page border frame

The script enforces 1-page output by default: if content overflows it retries
with progressively tighter font sizes until it fits.
"""
import sys, os, re, csv
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

W, H = A4

DEJAVU = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DEJAVU_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def register_fonts():
    if os.path.exists(DEJAVU):
        pdfmetrics.registerFont(TTFont("DV", DEJAVU))
        pdfmetrics.registerFont(TTFont("DV-Bold", DEJAVU_BOLD))
        return "DV", "DV-Bold"
    return "Helvetica", "Helvetica-Bold"


_FONT, _FONT_BOLD = register_fonts()


def build_styles(base_size=8.8):
    s = base_size
    INDIGO  = colors.HexColor("#4F46E5")
    VIOLET  = colors.HexColor("#7C3AED")
    INK     = colors.HexColor("#18181B")
    MUTED   = colors.HexColor("#52525B")
    return {
        "name":     ParagraphStyle("name",     fontName=_FONT_BOLD, fontSize=s*2.0, leading=s*2.4,
                                    spaceAfter=1, textColor=INDIGO, alignment=TA_CENTER),
        "contact":  ParagraphStyle("contact",  fontName=_FONT, fontSize=s*0.9, leading=s*1.3,
                                    spaceAfter=4, textColor=MUTED, alignment=TA_CENTER),
        "h2":       ParagraphStyle("h2",       fontName=_FONT_BOLD, fontSize=s*1.1, leading=s*1.5,
                                    spaceBefore=7, spaceAfter=2, textColor=VIOLET),
        "h3":       ParagraphStyle("h3",       fontName=_FONT_BOLD, fontSize=s*0.98, leading=s*1.35,
                                    spaceBefore=4, spaceAfter=0,
                                    textColor=colors.HexColor("#4338CA")),
        "sub":      ParagraphStyle("sub",      fontName=_FONT, fontSize=s*0.88, leading=s*1.25,
                                    spaceAfter=1, textColor=MUTED),
        "body":     ParagraphStyle("body",     fontName=_FONT, fontSize=s, leading=s*1.35,
                                    spaceAfter=1, textColor=INK),
        "bullet":   ParagraphStyle("bullet",   fontName=_FONT, fontSize=s, leading=s*1.35,
                                    spaceAfter=1, leftIndent=10, textColor=INK),
        "skill_row":ParagraphStyle("skill_row",fontName=_FONT, fontSize=s*0.9, leading=s*1.3,
                                    spaceAfter=2, textColor=INK),
    }


# ── contact parsing ──────────────────────────────────────────────────────────

ICON_EMAIL    = "\u2709"  # 
ICON_PHONE    = "\u260e"  # 
ICON_LOC      = "\u25c6"  # 
ICON_WEB      = "\u25c7"  # ◇ (open diamond — website)
ICON_GH       = "\u25c9"  # ◉ (circled dot — GitHub)
ICON_LI       = "\u25aa in"  #  in  (LinkedIn)
ICON_MEDIUM   = "\u25aa M"   # ▪ M (Medium — matches ▪ in LinkedIn pattern)


def _contact_item(raw):
    """Return (icon, display_text, href_or_None) for one raw contact token."""
    item = raw.strip()
    if not item:
        return None
    # Email
    if re.match(r'^[^@/\s]+@[^@]+\.[^@]+$', item):
        return (ICON_EMAIL, item, f"mailto:{item}")
    # Phone
    if re.match(r'^\+?[\d][\d\s\-\.\(\)]{5,}$', item):
        return (ICON_PHONE, item, None)
    # GitHub
    if 'github.com' in item:
        slug = item.rstrip('/').split('github.com/')[-1]
        url  = item if item.startswith('http') else f"https://{item}"
        return (ICON_GH, f"github/{slug}", url)
    # LinkedIn
    if 'linkedin.com' in item:
        slug = item.rstrip('/').split('/')[-1]
        url  = item if item.startswith('http') else f"https://{item}"
        return (ICON_LI, f"li/{slug}", url)
    # Medium
    if 'medium.com' in item:
        slug = item.rstrip('/').split('medium.com/')[-1]
        url = item if item.startswith('http') else f"https://{item}"
        return (ICON_MEDIUM, f"medium/{slug}", url)
    # Generic domain/URL  →  strip protocol, show bare domain
    if re.match(r'^(https?://)?(www\.)?[\w\-]+\.[a-z]{2,}', item):
        display = re.sub(r'^https?://', '', item).rstrip('/')
        url = item if item.startswith('http') else f"https://{item}"
        return (ICON_WEB, display, url)
    # Plain text = location
    return (ICON_LOC, item, None)


def _contact_fragment(icon, display, href):
    """Reportlab XML fragment for one contact item."""
    label = f"{icon}\u202f{display}"  # narrow no-break space after icon
    if href:
        return f'<a href="{href}" color="#4F46E5">{label}</a>'
    return label


def parse_contact_lines(lines, start):
    """
    Collect all '·'-separated contact tokens from consecutive lines after H1.
    Skips leading blank lines; stops at a blank line after content, or --- / #.
    Returns (items, next_i).
    """
    items = []
    i = start
    seen_content = False
    while i < len(lines):
        ln = lines[i].strip()
        if not ln:
            if seen_content:
                break   # blank line after contact block ends it
            i += 1
            continue    # skip leading blank lines before contact
        if ln.startswith('#') or ln.startswith('---'):
            break
        seen_content = True
        for tok in ln.split('\u00b7'):   # · U+00B7 middle dot
            parsed = _contact_item(tok)
            if parsed:
                items.append(parsed)
        i += 1
    return items, i


# ── headings.tsv icon map ────────────────────────────────────────────────────

def _load_headings():
    """Load data/headings.tsv → {lowercase_label: icon_char}."""
    for base in [os.path.dirname(os.path.abspath(__file__)), os.getcwd()]:
        p = os.path.join(base, 'data', 'headings.tsv')
        if os.path.exists(p):
            result = {}
            with open(p, encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter='\t')
                for row in reader:
                    icon = row.get('icon', '').strip()
                    if not icon or icon == '—':
                        continue
                    for col in ('es', 'en'):
                        label = row.get(col, '').strip()
                        if label and label != '—':
                            result[label.lower()] = icon
            return result
    return {}

_HEADINGS = _load_headings()


# ── inline markdown ──────────────────────────────────────────────────────────

def _escape(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def inline_fmt(text, font=None):
    f = font or _FONT
    fb = _FONT_BOLD
    text = _escape(text)
    text = re.sub(r'\*\*(.+?)\*\*', rf'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*',     rf'<i>\1</i>', text)
    text = re.sub(r'`(.+?)`',        r'<font name="Courier" size="7">\1</font>', text)
    return text


# ── skills inline (no columns) ───────────────────────────────────────────────

def build_skills_inline(rows, styles):
    """rows = list of (label_str, values_str). Full-width paragraphs, no table."""
    if not rows:
        return []
    flowables = []
    for label, value in rows:
        label_clean = re.sub(r'\*\*(.+?)\*\*', r'\1', label.strip()).rstrip(':')
        text = (f'<font color="#7C3AED"><b>{_escape(label_clean)}:</b></font>'
                f'\u2002{inline_fmt(value.strip())}')
        flowables.append(Paragraph(text, styles["skill_row"]))
    flowables.append(Spacer(1, 2))
    return flowables


# ── main renderer ─────────────────────────────────────────────────────────────

def md_to_flowables(md_text, styles, skip_sections=None):
    skip = {s.strip().lower() for s in (skip_sections or [])}
    flowables = []
    lines = md_text.splitlines()
    i = 0
    in_skipped = False
    skill_table_rows = []   # accumulate Markdown table rows
    in_skill_table = False

    def flush_skills():
        nonlocal skill_table_rows, in_skill_table
        if skill_table_rows:
            flowables.extend(build_skills_inline(skill_table_rows, styles))
        skill_table_rows = []
        in_skill_table = False

    while i < len(lines):
        line = lines[i]

        # ── skip metadata blockquote header ──────────────────────────────────
        if line.startswith('> '):
            i += 1
            continue

        # ── horizontal rule ──────────────────────────────────────────────────
        if line.strip() in ('---', '***', '___'):
            flush_skills()
            if not in_skipped:
                flowables.append(HRFlowable(width="100%", thickness=0.4,
                                            color=colors.HexColor("#cccccc"),
                                            spaceAfter=3, spaceBefore=2))
            i += 1
            continue

        # ── H1 : name + contact block ─────────────────────────────────────────
        if line.startswith('# '):
            flush_skills()
            in_skipped = False
            name = inline_fmt(line[2:].strip())
            flowables.append(Paragraph(name, styles["name"]))
            # collect contact lines that follow
            contact_items, i = parse_contact_lines(lines, i + 1)
            if contact_items:
                sep = '  \u2022  '   # ' • '
                frags = [_contact_fragment(*ci) for ci in contact_items]
                # Split into rows of max 4 items
                rows_txt = []
                for j in range(0, len(frags), 4):
                    rows_txt.append(sep.join(frags[j:j+4]))
                for row in rows_txt:
                    flowables.append(Paragraph(row, styles["contact"]))
            flowables.append(Spacer(1, 2))
            continue

        # ── H2 : section header ───────────────────────────────────────────────
        if line.startswith('## '):
            flush_skills()
            title = line[3:].strip()
            if title.lower() in skip:
                in_skipped = True
            else:
                in_skipped = False
                icon = _HEADINGS.get(title.lower(), '')
                prefix = f"{icon}\u2009" if icon else ''  # thin space after icon
                flowables.append(Paragraph(f"{prefix}{title.upper()}", styles["h2"]))
                flowables.append(HRFlowable(width="100%", thickness=0.8,
                                            color=colors.HexColor("#F43F5E"),
                                            spaceAfter=2, spaceBefore=0))
            i += 1
            continue

        if in_skipped:
            i += 1
            continue

        # ── H3 : job/project title ────────────────────────────────────────────
        if line.startswith('### '):
            flush_skills()
            flowables.append(Paragraph(inline_fmt(line[4:].strip()), styles["h3"]))
            i += 1
            continue

        # ── Markdown table ────────────────────────────────────────────────────
        if line.startswith('|') and '|' in line[1:]:
            in_skill_table = True
            if not re.match(r'^\|[-| :]+\|$', line):
                cells = [c.strip() for c in line.strip('|').split('|')]
                # Skip header row that is just 'Área' / 'Tecnologías'
                if cells[0].lower() not in ('área', 'area', 'categoría', 'categoria',
                                            'tecnologías', 'habilidad'):
                    if len(cells) >= 2:
                        skill_table_rows.append((cells[0], cells[1]))
            i += 1
            continue
        elif in_skill_table:
            flush_skills()

        # ── bullet ────────────────────────────────────────────────────────────
        if line.startswith('- '):
            flowables.append(Paragraph(
                f"\u2022 \u2009{inline_fmt(line[2:].strip())}",
                styles["bullet"]
            ))
            i += 1
            continue

        # ── non-empty plain text ──────────────────────────────────────────────
        if line.strip():
            # detect italic date/subtitle lines (start with *)
            if line.strip().startswith('*') and line.strip().endswith('*'):
                flowables.append(Paragraph(inline_fmt(line.strip()), styles["sub"]))
            else:
                flowables.append(Paragraph(inline_fmt(line.strip()), styles["body"]))

        i += 1

    flush_skills()
    return flowables


# ── page border ──────────────────────────────────────────────────────────────────────

_FRAME_COLOR = colors.HexColor("#312e81")  # dark indigo


def _draw_border(canvas, doc):
    """Draw a decorative dark-indigo frame around each page."""
    canvas.saveState()
    canvas.setFillColor(_FRAME_COLOR)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.rect(8, 8, W - 16, H - 16, fill=1, stroke=0)
    canvas.restoreState()


# ── page-count helper ────────────────────────────────────────────────────────────────

class _PageCounter:
    def __init__(self):
        self.count = 0
    def afterPage(self):
        self.count += 1
    def afterFlowable(self, flowable):
        pass
    onFirstPage = onLaterPages = lambda self, c, d: None


def _render(pdf_path, flowables, margin, base_size, border=True):
    from io import BytesIO
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=margin, rightMargin=margin,
        topMargin=margin * 0.9, bottomMargin=margin * 0.8,
    )
    cb = _draw_border if border else (lambda c, d: None)
    doc.build(flowables, onFirstPage=cb, onLaterPages=cb)
    # 1-page PDF: 1x /Type /Pages + 1x /Type /Page = 2 total occurrences
    pages = buf.getvalue().count(b'/Type /Page')
    if pages <= 2:
        with open(pdf_path, 'wb') as f:
            f.write(buf.getvalue())
        return True
    return False


def convert(md_path, pdf_path, skip_sections=None, border=True):
    with open(md_path, encoding="utf-8") as f:
        md_text = f.read()

    # Try progressively tighter settings until 1 page fits
    for base_size, margin_cm in [(8.8, 1.4), (8.3, 1.2), (7.8, 1.0), (7.3, 0.9)]:
        styles = build_styles(base_size)
        flowables = md_to_flowables(md_text, styles, skip_sections)
        if _render(pdf_path, flowables, margin_cm * cm, base_size, border):
            print(f"  OK  {pdf_path}  (size={base_size}pt, margin={margin_cm}cm)")
            return

    # Last resort: render whatever we have at tightest settings
    styles = build_styles(7.0)
    flowables = md_to_flowables(md_text, styles, skip_sections)
    doc = SimpleDocTemplate(
        pdf_path, pagesize=A4,
        leftMargin=0.9*cm, rightMargin=0.9*cm,
        topMargin=0.8*cm, bottomMargin=0.7*cm,
    )
    cb = _draw_border if border else (lambda c, d: None)
    doc.build(flowables, onFirstPage=cb, onLaterPages=cb)
    print(f"  WARN (overflow) {pdf_path}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', nargs='?', default='.')
    parser.add_argument('--skip-sections', default='',
                        help='Comma-separated section titles to omit, e.g. Idiomas,Resumen')
    parser.add_argument('--no-border', action='store_true',
                        help='Disable the decorative indigo page border frame')
    args = parser.parse_args()

    skip = [s for s in args.skip_sections.split(',') if s]
    border = not args.no_border
    folder = args.folder
    for fname in sorted(os.listdir(folder)):
        if fname.endswith('.md'):
            src = os.path.join(folder, fname)
            dst = os.path.join(folder, fname.replace('.md', '.pdf'))
            convert(src, dst, skip, border=border)
