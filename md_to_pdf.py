"""
Convert Markdown CVs to PDF using reportlab.
Usage: uv run --with reportlab --with markdown md_to_pdf.py <folder>
"""
import sys, os, re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

W, H = A4

def build_styles():
    base = getSampleStyleSheet()
    return {
        "h1": ParagraphStyle("h1", fontSize=18, leading=22, spaceAfter=4,
                              textColor=colors.HexColor("#1a1a2e"), fontName="Helvetica-Bold", alignment=TA_CENTER),
        "h2": ParagraphStyle("h2", fontSize=12, leading=15, spaceBefore=10, spaceAfter=3,
                              textColor=colors.HexColor("#1a5276"), fontName="Helvetica-Bold"),
        "h3": ParagraphStyle("h3", fontSize=10.5, leading=13, spaceBefore=6, spaceAfter=1,
                              textColor=colors.HexColor("#2c3e50"), fontName="Helvetica-Bold"),
        "body": ParagraphStyle("body", fontSize=9.5, leading=13, spaceAfter=2,
                               textColor=colors.HexColor("#2d2d2d"), fontName="Helvetica"),
        "bullet": ParagraphStyle("bullet", fontSize=9.5, leading=13, spaceAfter=2,
                                 leftIndent=12, bulletIndent=0,
                                 textColor=colors.HexColor("#2d2d2d"), fontName="Helvetica"),
        "meta": ParagraphStyle("meta", fontSize=9, leading=12, spaceAfter=6,
                               textColor=colors.HexColor("#555555"), fontName="Helvetica", alignment=TA_CENTER),
        "blockquote": ParagraphStyle("blockquote", fontSize=8, leading=11, spaceBefore=0, spaceAfter=6,
                                     leftIndent=10, textColor=colors.HexColor("#888888"),
                                     fontName="Helvetica-Oblique"),
    }


def inline_fmt(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'`(.+?)`', r'<font name="Courier" size="8">\1</font>', text)
    text = text.replace('&', '&amp;').replace('<b>', '<b>').replace('</b>', '</b>')
    return text


def md_to_flowables(md_text, styles):
    flowables = []
    lines = md_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]

        # Skip blockquote lines (metadata header in our CVs)
        if line.startswith('> '):
            text = line[2:].strip()
            if text:
                flowables.append(Paragraph(inline_fmt(text), styles["blockquote"]))
            i += 1
            continue

        # Horizontal rule
        if line.strip() in ('---', '***', '___'):
            flowables.append(Spacer(1, 4))
            flowables.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
            flowables.append(Spacer(1, 4))
            i += 1
            continue

        # H1
        if line.startswith('# '):
            flowables.append(Paragraph(inline_fmt(line[2:].strip()), styles["h1"]))
            i += 1
            continue

        # H2
        if line.startswith('## '):
            flowables.append(Paragraph(inline_fmt(line[3:].strip()), styles["h2"]))
            i += 1
            continue

        # H3
        if line.startswith('### '):
            flowables.append(Paragraph(inline_fmt(line[4:].strip()), styles["h3"]))
            i += 1
            continue

        # Table (| ... |)
        if line.startswith('|') and '|' in line[1:]:
            table_lines = []
            while i < len(lines) and lines[i].startswith('|'):
                if not re.match(r'^\|[-| :]+\|$', lines[i]):
                    cells = [c.strip() for c in lines[i].strip('|').split('|')]
                    table_lines.append(cells)
                i += 1
            if table_lines:
                col_count = max(len(r) for r in table_lines)
                data = []
                for row in table_lines:
                    while len(row) < col_count:
                        row.append('')
                    data.append([Paragraph(inline_fmt(c), styles["body"]) for c in row])
                col_w = (W - 4*cm) / col_count
                t = Table(data, colWidths=[col_w]*col_count)
                t.setStyle(TableStyle([
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0,0), (-1,-1), 9),
                    ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.HexColor("#f8f9fa"), colors.white]),
                    ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor("#dddddd")),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                    ('TOPPADDING', (0,0), (-1,-1), 4),
                ]))
                flowables.append(t)
                flowables.append(Spacer(1, 4))
            continue

        # Bullet
        if line.startswith('- '):
            text = inline_fmt(line[2:].strip())
            flowables.append(Paragraph(f"&#8226; &nbsp;{text}", styles["bullet"]))
            i += 1
            continue

        # Bold italic line (like **Role** — Company)
        if line.strip():
            flowables.append(Paragraph(inline_fmt(line.strip()), styles["body"]))

        i += 1

    return flowables


def convert(md_path, pdf_path, styles):
    with open(md_path, encoding="utf-8") as f:
        md_text = f.read()

    doc = SimpleDocTemplate(
        pdf_path, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=1.8*cm, bottomMargin=1.8*cm,
    )
    flowables = md_to_flowables(md_text, styles)
    doc.build(flowables)
    print(f"  OK  {pdf_path}")


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "."
    styles = build_styles()
    for fname in sorted(os.listdir(folder)):
        if fname.endswith(".md"):
            src = os.path.join(folder, fname)
            dst = os.path.join(folder, fname.replace(".md", ".pdf"))
            convert(src, dst, styles)
