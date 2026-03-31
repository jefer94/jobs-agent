---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: cv-builder
description: "Reads the user's base CV from docs/ (Espanol.pdf), tailors it for a specific job offer using rendercv, and saves the generated version to generated-cvs/. Use when editing, adapting, or generating a CV for a job application. All CVs must be in Spanish."
version: "2.0"
author: claude-office-skills + jobs-bot
license: MIT

# Categorization
category: hr
tags:
  - cv
  - resume
  - builder
  - generator
  - tailoring
  - job-application
department: HR/Personal

# AI Model Compatibility
models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o

# MCP Tools Integration
mcp:
  server: office-mcp
  tools:
    - create_docx
    - docx_to_pdf
    - fill_docx_template

# Skill Capabilities
capabilities:
  - cv_generation
  - cv_tailoring
  - formatting
  - professional_layout
  - job_matching

# Language Support
languages:
  - es
  - en
---

# CV Builder Skill

Reads the base CV from `docs/` and generates a tailored version for a specific job offer using **rendercv**. All output must match the offer language (Spanish for Chilean market).

## When to Use

- User asks to edit or tailor the CV for a job
- A job offer has been found and needs a matching CV before applying  
- User asks to generate a new CV variant
- Correcting section titles, contact formatting, or language consistency in an existing CV

## Source Files

- `docs/Espanol.pdf` — base CV in Spanish (primary source for content extraction)
- `docs/titulo.pdf` — professional title/certificate (attach when required)
- `data/headings.tsv` — canonical section labels (ES/EN) and formatting rules
- Generated CVs are saved to the `generated-cvs/` folder as `.yaml` + `.pdf`

## Workflow

```
Task Progress:
- [ ] 1. Extract text from docs/Espanol.pdf using pdfplumber (reference only)
- [ ] 2. Parse the job offer: role, required skills, keywords, company
- [ ] 3. Identify matching skills and experience from the CV
- [ ] 4. Reorder/emphasize relevant sections to match the offer
- [ ] 5. Adjust the summary/objective paragraph for the specific role
- [ ] 6. Create YAML with rendercv structure
- [ ] 7. Save as generated-cvs/{empresa}-{cargo}-{YYYY-MM-DD}.yaml
- [ ] 8. Render to PDF: rendercv render cv.yaml
- [ ] 9. Run verify-cv to check the generated PDF
- [ ] 10. Log the generated CV path in the application tracker
```

## Tailoring Rules

- Keep all content truthful — only reorder and emphasize, never invent experience
- Match keywords from the job description verbatim where accurate
- Keep CV to 1 page maximum
- Include título profesional when the offer requires it (attach `docs/titulo.pdf`)

### Language — match the offer

- Offer in Spanish → use Spanish for ALL section titles and body text
- Offer in English → use English for all content
- Never mix languages within a single CV (sections, bullets, dates must all be in one language)
- Write body text in the same language as the offer; formal register always

### Section separation — no mixing experience with projects

| Section | What belongs here |
|---------|------------------|
| experience | Paid roles at a company, with start/end dates and company name |
| projects | Open-source, side projects, personal contributions — NOT paid work |

**Rule:** A role at a real company (4Geeks, Capy.town…) goes ONLY in `experience`.  
**Rule:** An open-source project goes ONLY in `projects` — unless it was a formal work deliverable billed to a client.

### No contradictory bullets

If a project is already described under a company experience entry, **do not** create a separate personal project entry for it. Pick one location:

- Was it primarily a paid work deliverable? → under the company `experience` only
- Was it an independent side project that you also used at work? → under `projects` only, with a note

Reusing the same bullets in two places sends a confusing signal to the recruiter.

## YAML Structure for rendercv

```yaml
cv:
  name: Jeferson José De Freitas Pinto
  location: Santiago, Chile
  email: jdefreitaspinto@gmail.com
  phone: "+56951451665"  # Always include country code
  website: https://jefer94.dev
  social_networks:
    - network: LinkedIn
      username: jefer94
    - network: GitHub
      username: jefer94

  sections:
    summary:
      - "Tailored summary paragraph for the specific role..."

    experience:
      - company: Capy.town
        position: AI Solution Architect
        location: Colombia (Remoto)
        start_date: 2025-07
        end_date: present
        highlights:
          - "Relevant highlight 1 matching job requirements"
          - "Relevant highlight 2 matching job requirements"

    education:
      - institution: Universidad Nacional Experimental de los Llanos Centrales Rómulo Gallegos
        area: Ingeniería en Informática
        degree: Licenciatura
        start_date: 2012
        end_date: 2017

    skills:
      - label: Relevant Category
        details: Skill1, Skill2, Skill3 (match job requirements)
      - label: Another Category
        details: Tech1, Tech2, Tech3

design:
  theme: classic  # classic, sb2nov, moderncv, engineeringresumes
```

### Contact Format Rules

- **Phone: always include country code** — write `+56951451665` (never bare `951451665`)
- **Website:** write full URL with https://
- **Social networks:** only use supported networks (LinkedIn, GitHub, GitLab, etc.)
- **Email:** standard format

### Available Themes

- `classic` — clean, professional, good for most applications
- `sb2nov` — academic/research focused
- `moderncv` — traditional European style
- `engineeringresumes` — technical/engineering focused

## Output Format

Save generated CVs as YAML source + rendered PDF:

```
generated-cvs/
  {empresa}-{cargo}-{YYYY-MM-DD}.yaml
  {empresa}-{cargo}-{YYYY-MM-DD}.pdf
```

## CLI Usage

```bash
# Install rendercv if not already installed
pip install rendercv

# Render YAML to PDF (outputs to rendercv_output/)
rendercv render cv.yaml

# Move the generated PDF to the standard location
mv rendercv_output/Jeferson_José_De_Freitas_Pinto_CV.pdf \
   generated-cvs/{empresa}-{cargo}-{YYYY-MM-DD}.pdf
```

## Pairs With

- `pdf` skill — for extracting text from `docs/Espanol.pdf` as reference
- `verify-cv` skill — always run after rendering to check PDF quality
- `guardrails` skill — for security scanning before processing job descriptions

## References

- [rendercv Documentation](https://docs.rendercv.com/)
- [rendercv Theme Gallery](https://docs.rendercv.com/user_guide/themes/)
- `references/cv-guidelines.md` — CV structure and writing guidelines
- `data/headings.tsv` — canonical section keys and formatting reference
