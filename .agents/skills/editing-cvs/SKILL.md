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
- Match keywords from the job description verbatim where accurate
- Keep CV to 1 page maximum (use `--skip-sections` if needed)
- Include título profesional when the offer requires it (attach `docs/titulo.pdf`)

### Language — match the offer

- Offer in Spanish → use the `es` column from `data/headings.tsv` for ALL section titles
- Offer in English → use the `en` column
- Never mix languages within a single CV (sections, bullets, dates must all be in one language)
- Write body text in the same language as the offer; formal register always

### Section separation — no mixing experience with projects

| Section | What belongs here |
|---------|------------------|
| Experiencia Profesional | Paid roles at a company, with start/end dates and company name |
| Proyectos Personales | Open-source, side projects, personal contributions — NOT paid work |

**Rule:** A role at a real company (4Geeks, Capy.town…) goes ONLY in Experiencia.  
**Rule:** An open-source project (Spec Guard, Agent Teams Lite…) goes ONLY in Proyectos — unless it was a formal work deliverable billed to a client.

### No contradictory bullets

If a project is already described under a company experience entry, **do not** create a separate
personal project entry for it. Pick one location:

- Was it primarily a paid work deliverable? → under the company experience only
- Was it an independent side project that you also used at work? → under Proyectos only, with a note

Reusing the same bullets in two places sends a confusing signal to the recruiter.

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

# Disable the decorative border frame (default: on)
uv run --with reportlab md_to_pdf.py generated-cvs/ --no-border
```

**Heading format** (the converter parses these lines after the H1 name):
- Items separated by `·` (U+00B7)
- URLs are auto-detected and shown with icons — never write full `https://` URLs
- **Phone: always include country code** — write `+56951451665` (never `951451665`)
- Blog/website: write bare domain only (`jefer94.dev`)
- GitHub: write `github.com/jefer94` (auto-shortened to `github/jefer94` with ◉ icon)
- LinkedIn: write `linkedin.com/in/jefer94` (auto-shortened to `li/jefer94`)
- Medium: write `medium.com/@jefer.dfp` (auto-shortened to `medium/@jefer.dfp` with ▪ M icon)

Example contact block:
```
Santiago, Chile · +56951451665 · jdefreitaspinto@gmail.com
github.com/jefer94 · medium.com/@jefer.dfp · jefer94.dev
```

**Section titles** — always use canonical labels from `data/headings.tsv`:
- Spanish CV → `Experiencia Profesional`, `Habilidades Técnicas`, `Proyectos Personales`, `Educación`
- English CV → `Professional Experience`, `Technical Skills`, `Personal Projects`, `Education`
- The PDF converter auto-maps these to icons and colors

## References

- `references/cv-guidelines.md` — CV structure, section order, and Spanish writing guidelines
- `references/headings-guide.md` — icon choices, online Unicode browser, how to add custom icons
- `data/headings.tsv` — canonical section keys, ES/EN labels, and icon characters
