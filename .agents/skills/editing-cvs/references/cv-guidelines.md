# CV Guidelines — Spanish Format

Structure, section order, and writing conventions for Chilean job market CVs.

## Standard CV Structure (Chilean market)

1. **Datos personales** — Name, city, phone, email, LinkedIn (no RUT or photo required)
2. **Resumen profesional** — 3–4 sentences tailored to the specific role
3. **Experiencia laboral** — Reverse chronological, last 10 years
4. **Educación** — Degree, institution, year of graduation
5. **Habilidades técnicas** — Hard skills, tools, technologies
6. **Habilidades blandas** — Soft skills (brief, 4–6 items max)
7. **Idiomas** — Spanish: nativo, English: level
8. **Certificaciones** (optional) — Only if relevant to the role

## Section Writing Rules

### Resumen profesional
- Start with role title: "Desarrollador Backend con X años de experiencia en..."
- Mention 2–3 key technologies or domains from the job offer
- End with a value proposition: "...orientado a resolver problemas de alto impacto en equipos ágiles"

### Experiencia laboral
Format each entry:
```
**{Cargo}** — {Empresa}, {Ciudad} ({mes/año} – {mes/año o Presente})
- Logro concreto con métrica si es posible (ej: "Reduje tiempos de carga en 40%")
- Responsabilidad alineada con el cargo postulado
- Tecnología o herramienta relevante utilizada
```

Use **action verbs in past tense** (desarrollé, implementé, lideré, optimicé, diseñé).

### Habilidades técnicas
Group by category:
```
**Lenguajes:** Python, JavaScript, SQL
**Frameworks:** FastAPI, React, Django
**Herramientas:** Docker, Git, PostgreSQL
**Cloud:** AWS (S3, Lambda, EC2)
```

## Spanish Writing Conventions

- Formal register: use "usted" forms in cover letters, avoid slang
- Avoid Anglicisms unless they are industry-standard terms (e.g., "sprint", "deploy")
- Numbers: use period as thousands separator (1.000.000), comma as decimal (3,14)
- Dates: "enero de 2023" (lowercase month)

## Keyword Matching Strategy

1. Extract all nouns and technical terms from the job description
2. Find which ones are present (truthfully) in the base CV
3. Insert matching keywords naturally — in the summary, skills section, or experience bullets
4. **Never add keywords for skills you don't have**

## File Naming Convention

```
generated-cvs/{empresa}-{cargo_normalizado}-{YYYY-MM-DD}.md
```

Normalize cargo: lowercase, spaces → hyphens, remove accents
Example: `empresa-sa-desarrollador-backend-2024-01-15.md`

## PDF Generation

If a PDF is needed, convert from Markdown using `pandoc`:

```bash
pandoc cv.md -o cv.pdf --pdf-engine=weasyprint
```

Or use Python `markdown-pdf`:
```bash
pip install markdown-pdf
```
