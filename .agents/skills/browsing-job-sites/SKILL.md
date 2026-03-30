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
- [ ] 2. Prompt user for credentials at startup (see Credentials section)
- [ ] 3. Open one browser context per portal in parallel (see Browser Setup)
- [ ] 4. Log into each portal — use Google/LinkedIn OAuth where available
- [ ] 5. Search all portals simultaneously with Spanish keywords from CV
- [ ] 6. Filter: language=Spanish, location=Chile, posted=last 7 days
- [ ] 7. Score each offer against CV (relevance check)
- [ ] 8. For relevant offers: open offer page (max 1 per portal at a time), verify Spanish, apply
- [ ] 9. Close offer page before opening the next one on that portal
- [ ] 10. Log application to tracking store (see tracking-applications skill)
```

## Key Rules

- **Only apply to offers written entirely in Spanish** — skip if description contains English
- Never apply to the same offer twice — check tracking store before applying
- Prefer offers that match at least 2 skills from the CV
- If a CAPTCHA appears, pause and ask the user for help

## Browser Setup

Use Playwright with `chromium` in **headed mode** (`headless: False`). Open **one persistent browser context per portal** so all portals run in parallel. Each context keeps **at most 1 job offer page open at a time** to avoid bot detection.

```python
from playwright.sync_api import sync_playwright
import threading

PORTALS = ["linkedin", "trabajando", "laborum", "getonbrd", "computrabajo", "indeed"]

def run_portal(portal_name, creds, browser):
    session_path = f".sessions/{portal_name}.json"
    ctx = browser.new_context(
        storage_state=session_path if os.path.exists(session_path) else None
    )
    # login → search → apply loop (max 1 offer page open at a time)
    ...

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=["--start-maximized"])
    threads = [threading.Thread(target=run_portal, args=(name, creds, browser))
               for name in PORTALS]
    for t in threads: t.start()
    for t in threads: t.join()
```

Save each portal's session to `.sessions/{portal}.json` after login to skip re-login on next run.

## Credentials

**Never read credentials from `.env` or any file** — the AI could read and leak them.

At startup, prompt the user interactively for each site's password. Credentials live only in memory for the session duration:

```python
import getpass

def prompt_credentials():
    print("Enter credentials (input is hidden):")
    creds = {}
    for site in ["trabajando", "laborum", "getonbrd", "computrabajo", "indeed"]:
        creds[site] = {
            "password": getpass.getpass(f"  {site} password: ")
        }
    return creds
```

- **LinkedIn and Google:** use OAuth sign-in with `jdefreitaspinto@gmail.com` — no password prompt needed for those
- Session cookies saved to `.sessions/` skip re-login until the session expires
- If a saved session is still valid, no prompt is shown for that portal

## References

- `references/job-sites.md` — login flows, search selectors, and apply button locators per site
