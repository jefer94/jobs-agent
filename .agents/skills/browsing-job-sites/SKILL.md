---
name: browsing-job-sites
description: Controls Chrome to log into Chilean job sites (LinkedIn, Trabajando.cl, Laborum.cl, GetOnBoard, CompuTrabajo, Indeed Chile), search for Spanish-language job offers matching the user's CV, and automate job applications. Use when searching for jobs, browsing job sites, or applying to offers in Chile.
---

# Browsing Job Sites

Automates Chrome to interact with Chilean job portals and Google Jobs. Finds Spanish-language offers matching the CV in `docs/` and submits applications.

## When to Use

- User asks to search for jobs or find job offers
- User asks to apply to job postings
- User asks to log into a job site
- User wants to scan new offers in Chile

## Target Sites

See `references/job-sites.md` for login URLs, selectors, and quirks per site.

- **LinkedIn** — linkedin.com/jobs (filter: Chile, Spanish)
- **Trabajando.cl** — trabajando.com
- **Laborum.cl** — laborum.cl
- **GetOnBoard** — getonbrd.com (tech-focused)
- **CompuTrabajo Chile** — cl.computrabajo.com
- **Indeed Chile** — cl.indeed.com
- **Google Jobs** — google.com/search?q=ofertas+trabajo (via Google search)

## Workflow

```
Task Progress:
- [ ] 1. Read CV from docs/ to extract skills, role, and keywords
- [ ] 2. Open Chrome via Playwright (chromium, headful)
- [ ] 3. Log into target site (load saved session or credentials from .env)
- [ ] 4. Search with Spanish keywords derived from CV
- [ ] 5. Filter: language=Spanish, location=Chile, posted=last 7 days
- [ ] 6. Score each offer against CV (relevance check)
- [ ] 7. For relevant offers: open, verify Spanish language, apply
- [ ] 8. Log application to tracking store (see tracking-applications skill)
```

## Key Rules

- **Only apply to offers written entirely in Spanish** — skip if description contains English
- Never apply to the same offer twice — check tracking store before applying
- Prefer offers that match at least 2 skills from the CV
- If a CAPTCHA appears, pause and ask the user for help

## Browser Setup

Use Playwright with `chromium` in **headed mode** (`headless: false`) so the user can observe and intervene.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=["--start-maximized"])
    context = browser.new_context(storage_state=".sessions/session.json")
    page = context.new_page()
```

Save session state after login to `.sessions/session.json` to avoid re-logging every run.

## Credentials

Store credentials in `.env` (never hardcode):
```
LINKEDIN_EMAIL=
LINKEDIN_PASSWORD=
TRABAJANDO_EMAIL=
TRABAJANDO_PASSWORD=
```

## References

- `references/job-sites.md` — login flows, search selectors, and apply button locators per site
