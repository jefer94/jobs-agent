---
name: editing-cvs
description: Reads the user's base CV from docs/ (Espanol.pdf), tailors it for a specific job offer, and saves the generated version. Use when editing, adapting, or generating a CV for a job application. All CVs must be in Spanish.
---

# Editing CVs

Reads the base CV from `docs/` and generates a tailored version for a specific job offer. All output must be in Spanish.

## When to Use

- User asks to edit or tailor the CV for a job
- A job offer has been found and needs a matching CV before applying
- User asks to generate a new CV variant

## Source Files

- `docs/Espanol.pdf` — base CV in Spanish (primary source)
- `docs/titulo.pdf` — professional title/certificate (attach when required)
- Generated CVs are saved to the `generated-cvs/` folder

## Workflow

```
Task Progress:
- [ ] 1. Extract text from docs/Espanol.pdf using pdfplumber
- [ ] 2. Parse the job offer: role, required skills, keywords, company
- [ ] 3. Identify matching skills and experience from the CV
- [ ] 4. Reorder/emphasize relevant sections to match the offer
- [ ] 5. Adjust the summary/objective paragraph for the specific role
- [ ] 6. Save as generated-cvs/{company}-{role}-{date}.md (and/or .pdf)
- [ ] 7. Log the generated CV path in the application tracker
```

## Tailoring Rules

- Keep all content truthful — only reorder and emphasize, never invent experience
- Always write in Spanish (formal register, tuteo avoided)
- Match keywords from the job description verbatim where accurate
- Keep CV to 1–2 pages maximum
- Include título profesional when the offer requires it (attach `docs/titulo.pdf`)

## Extract PDF Text

```python
import pdfplumber

with pdfplumber.open("docs/Espanol.pdf") as pdf:
    text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
```

## Output Format

Save generated CVs as Markdown first (easier to edit), then convert to PDF:

```
generated-cvs/
  {empresa}-{cargo}-{YYYY-MM-DD}.md
  {empresa}-{cargo}-{YYYY-MM-DD}.pdf
```

## Convert Markdown → PDF

Use `md_to_pdf.py` at the project root (requires `reportlab`):

```bash
# Convert all .md files in a folder to PDF (enforces 1-page automatically)
uv run --with reportlab md_to_pdf.py generated-cvs/

# Drop optional sections to save space (e.g., Idiomas, Resumen)
uv run --with reportlab md_to_pdf.py generated-cvs/ --skip-sections "Idiomas,Resumen"
```

**Heading format** (the converter parses these lines after the H1 name):
- Items separated by `·` (U+00B7)
- URLs are auto-detected and shown with icons — never write full `https://` URLs
- Blog/website: write bare domain only (`jefer94.dev`)
- GitHub: write `github.com/jefer94` (auto-shortened to `github/jefer94` with ⊙ icon)
- LinkedIn: write `linkedin.com/in/jefer94` (auto-shortened to `li/jefer94`)

## References

- `references/cv-guidelines.md` — CV structure, section order, and Spanish writing guidelines
