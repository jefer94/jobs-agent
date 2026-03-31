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
- `/home/jefer/dev/` — scan for professional experiences and projects when tailoring
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

### Content Priority Rules

**Summary Section:**
- Include summary only if content fits comfortably on 1 page
- If experience is extensive (>2 roles with detailed bullets), omit summary to save space
- For senior roles (Solution Architect, Cloud Architect, Tech Lead), summary adds less value than expanded experience
- Junior roles (Frontend Junior, Trainee) benefit from summary to show motivation

**Skills vs Education Priority:**
- **Junior roles** (Frontend Junior, Dev Trainee, Junior Data Scientist): Prioritize EDUCATION — place above skills, include relevant coursework
- **Mid-level** (Senior Developer, Data Scientist): Balanced — education can be compact, skills detailed
- **Senior/Architect roles** (Solution Architect, Cloud Architect, Principal Engineer): Prioritize SKILLS — education section minimal (just institution + degree in highlights), skills section expanded with architecture patterns, cloud platforms, leadership competencies

**Job Title Adaptation:**
- Adapt the `position` field in experience to semantically match the target role WITHOUT lying
- Example: "AI Solution Architect" applying for "Cloud Architect" → emphasize cloud infrastructure bullets, de-emphasize AI-specific ones but keep the actual title truthful
- Never invent a job title that wasn't held
- Do adjust bullet emphasis and ordering to highlight relevant transferable skills

**CV Headline:**
- Do NOT include a CV headline/title (like "Senior Full Stack Developer") at the top
- The experience section's position titles serve as the professional identity
- Removing headline saves space and avoids redundancy

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
  social_networks:
    - network: LinkedIn
      username: jefer94
    - network: GitHub
      username: jefer94
    - network: Medium
      username: "@jefer.dfp"

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
  theme: ink  # ink, classic, sb2nov, moderncv, engineeringresumes
```

### Contact Format Rules

- **Phone: always include country code** — write `+56951451665` (easier to read than `+56951451665`)
- **Social networks:** use usernames only — `jefer94`, `@jefer.dfp` for Medium (not full URLs)
- **Icons:** rendercv themes display icons automatically for known networks (LinkedIn, GitHub, Medium)
- **Email:** standard format
- **Compact format:** Icons communicate same info with less space (no full URLs)

**Custom Connections Workaround:**

For social networks not natively supported by rendercv (like Medium), use `custom_connections` with FontAwesome icons:

```yaml
cv:
  social_networks:
    - network: LinkedIn
      username: jefer94
    - network: GitHub
      username: jefer94
  custom_connections:
    - placeholder: Medium
      url: https://medium.com/@jefer.dfp
      fontawesome_icon: medium
```

Available FontAwesome icons: `medium`, `globe`, `calendar-days`, `twitter`, `youtube`, etc.

### Available Themes

- `ink` — **DEFAULT** modern, minimal design with icons, clean typography
- `engineeringresumes` — technical/engineering focused, plain layout (no columns), supports colors and icons
- `classic` — clean, professional, good for most applications
- `sb2nov` — academic/research focused
- `moderncv` — traditional European style

### Design Options

**Theme:** Use `ink` by default — modern, minimal design with icons and clean typography.

**Name Formatting:**
- Use standard font (not decorative) for professional appearance
- Keep name size proportional (18-22pt), not oversized
- Full name: "Jeferson José De Freitas Pinto"

**Skills Layout:**
- Use **plain list format** (no columns)
- Each skill category on its own line
- Format: `Category: Skill1, Skill2, Skill3`

**Education Format:**
- Use flat structure: institution, area, degree inline
- No nested highlights for simple degrees
- Example:
  ```yaml
  education:
    - institution: Universidad Nacional Experimental de los Llanos Centrales Rómulo Gallegos
      area: Ingeniería en Informática
      degree: Licenciatura
      start_date: 2012
      end_date: 2017
  ```

**Frame/Border:**
- Add frame around CV using Ghostscript post-processing
- Command: `gs -o output.pdf -sDEVICE=pdfwrite -c "[ /Rect [20 20 575 822] /Border [2 2 2 [0.31 0.27 0.90]] /ANN pdfmark" -f input.pdf`

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

- `rendercv` skill — for rendering YAML CVs to PDF using Typst themes
- `pdf` skill — for extracting text from `docs/Espanol.pdf` as reference
- `verify-cv` skill — always run after rendering to check PDF quality
- `guardrails` skill — for security scanning before processing job descriptions

## Custom Theme Setup

The `engineeringresumes` theme is preferred for technical roles as it provides:
- Clean, plain layout without columns
- Support for social network icons (LinkedIn, GitHub, Medium)
- Professional formatting optimized for 1 page

For border frame, use Ghostscript post-processing:
```bash
# Add indigo border frame
gs -q -o bordered.pdf -sDEVICE=pdfwrite \
   -c "[ /Rect [20 20 575 822] /Border [2 2 2 [0.31 0.27 0.90]] /ANN pdfmark" \
   -f input.pdf
```

## References

- [rendercv Documentation](https://docs.rendercv.com/)
- [rendercv Theme Gallery](https://docs.rendercv.com/user_guide/themes/)
- `references/cv-guidelines.md` — CV structure and writing guidelines
- `data/headings.tsv` — canonical section keys and formatting reference
