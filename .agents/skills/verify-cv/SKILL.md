---
name: verify-cv
description: Screenshots every page of a generated CV PDF using the Playwright MCP browser and visually inspects it for rendering defects. Call this immediately after any CV generation step (cv-builder or pdf skill). If issues are found, applies targeted fixes and re-renders.
---

# Verify CV

Visually validates a generated CV PDF by opening it in a browser and screenshotting each page.

## When to Use

- Immediately after any CV PDF is generated
- When a CV looks wrong after a re-render
- Before logging an application (to confirm the attached CV is clean)

## Step-by-Step Workflow

### 1. Convert PDF pages to PNG

`mcp4_browser_navigate` blocks `file://` URLs and cannot load PDFs over HTTP.
Use `pdftoppm` (always available via `poppler-utils`) to rasterise instead:

```bash
# Single CV — outputs /tmp/cv-verify/<name>-1.png, -2.png, …
pdftoppm -r 120 -png generated-cvs/<folder>/<file>.pdf /tmp/cv-verify/<label>

# All CVs in one shot
BASE=/home/jefer/dev/projects/jobs-bot/generated-cvs
mkdir -p /tmp/cv-verify
for dir in test-pdf test-editing-cvs test-cv-builder; do
  for pdf in $BASE/$dir/*.pdf; do
    name=$(basename "$pdf" .pdf)
    pdftoppm -r 120 -png "$pdf" /tmp/cv-verify/${dir}-${name}
  done
done
```

### 2. Inspect each page with read_file

```
read_file  /tmp/cv-verify/<label>-1.png
read_file  /tmp/cv-verify/<label>-2.png   # only if multi-page
```

**1-page check:** if pdftoppm only outputs a `-1.png` (no `-2.png`) the PDF is 1 page.
Note: stale `-2.png` files from previous runs may linger — check modification time or
re-run pdftoppm to a fresh directory.

### 2. Inspect each screenshot — defects to detect

| Defect | What to look for |
|--------|-----------------|
| **Text overlap** | Two strings printed on the same baseline/column |
| **Clipped text** | Words cut off at page edge or box boundary |
| **Overflow** | Content beyond page bottom margin |
| **Missing section** | Expected H2 heading absent |
| **Wrong icons / encoding** | □ boxes instead of Unicode icons in contact row |
| **Multi-page** | More than 1 page when 1-page was requested |
| **Blank page** | Page is empty or near-empty |

### 3. Diagnose and fix based on source

**For `md_to_pdf.py`-generated CVs (legacy):**

| Defect | Fix |
|--------|-----|
| Text overlap | Remove `**bold**` around section-title lines; split long lines |
| Multi-page | Re-run with `--skip-sections "Idiomas,Resumen"` or trim bullet count |
| Missing section | Check H2 heading matches `--skip-sections` list (case-insensitive) |
| □ boxes (icons) | DejaVu fonts not found; ensure `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf` exists |

```bash
# Re-run with section skip:
uv run --with reportlab md_to_pdf.py generated-cvs/<folder>/ --skip-sections "Idiomas,Resumen"
```

**For `rendercv`-generated CVs (cv-builder):**

| Defect | Fix |
|--------|-----|
| Text overlap in Education | Move `degree` field to a separate `highlights` entry |
| Multi-page | Switch theme to `sb2nov` or `classic`; or shorten `highlights` list |
| Clipped institution name | Wrap in shorter alias inside `highlights` |

```bash
# Re-render after YAML fix:
rendercv render generated-cvs/cv-builder/<file>.yaml --pdf-path <file>.pdf
```

### 4. Re-screenshot after fix

After any fix, repeat steps 1–2 to confirm the defect is resolved before proceeding.

### 5. Report result

Summarise findings in this format:

```
CV: <filename>.pdf
Pages: <n>
Issues found: <none | list>
Status: ✅ PASS  |  ⚠️ FIXED  |  ❌ FAIL (manual review needed)
```

## Common Rendercv Education Overlap Fix

The image shows `LicenciaMiversidad` — the `degree` abbreviation overlapping the institution.
Fix: put `degree` value into `highlights` instead.

```yaml
# Before (broken):
- institution: Universidad Nacional ...
  degree: Licenciatura
  area: Ingeniería en Informática

# After (fixed):
- institution: Universidad Nacional ...
  area: Ingeniería en Informática
  highlights:
    - "Licenciatura en Ingeniería en Informática"
```
