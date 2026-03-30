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

Save generated CVs as Markdown first (easier to edit), then convert to PDF if needed:

```
generated-cvs/
  {empresa}-{cargo}-{YYYY-MM-DD}.md
  {empresa}-{cargo}-{YYYY-MM-DD}.pdf  (optional)
```

## References

- `references/cv-guidelines.md` — CV structure, section order, and Spanish writing guidelines
