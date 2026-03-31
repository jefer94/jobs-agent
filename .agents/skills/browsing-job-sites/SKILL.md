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

- **LinkedIn** — linkedin.com/jobs (filter: `{market}` / `{language}` from `data/targets.tsv`)
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
- [ ] 5. Search all portals simultaneously with keywords from CV in `{language}` from `data/targets.tsv`
- [ ] 6. Filter: language=`{language}`, location=`{market}` (from `data/targets.tsv`), posted=last 7 days
- [ ] 7. Score each offer against CV (relevance check)
- [ ] 8. For relevant offers: open offer page (max 1 per portal at a time), verify Spanish, apply
- [ ] 9. Close offer page before opening the next one on that portal
- [ ] 10. Log application to tracking store (see tracking-applications skill)
```

## Key Rules

- **Only apply to offers in the target language** — read `language` from `data/targets.tsv`; skip if detected language differs
- Never apply to the same offer twice — check tracking store before applying
- Prefer offers that match at least 2 skills from the CV
- If a CAPTCHA appears, pause and ask the user for help

## Browser Setup

Use the **Playwright MCP tools** (`mcp4_browser_*`) — do NOT write Python Playwright code. The MCP server controls a single headed Chrome instance. Open **one tab per portal** and switch between them with `mcp4_browser_tabs`.

### Open tabs for each portal
```
1. mcp4_browser_tabs action=new  → linkedin tab (index 0)
2. mcp4_browser_tabs action=new  → trabajando tab (index 1)
3. mcp4_browser_tabs action=new  → laborum tab (index 2)
4. mcp4_browser_tabs action=new  → getonbrd tab (index 3)
5. mcp4_browser_tabs action=new  → computrabajo tab (index 4)
6. mcp4_browser_tabs action=new  → indeed tab (index 5)
```

### Per-portal loop (repeat for each tab)
```
1. mcp4_browser_tabs action=select index={n}
2. Login (OAuth or typed credentials — see Credentials)
3. mcp4_browser_navigate to search URL with CV keywords
4. mcp4_browser_snapshot  → scan offer cards
5. For each offer:
   a. mcp4_browser_click  → open offer (max 1 at a time)
   b. mcp4_browser_snapshot  → read description, verify Spanish
   c. If Spanish + relevant: apply (fill form, click submit)
   d. mcp4_browser_tabs action=close current offer tab (if opened in new tab)
   e. Wait 3-5s before next offer
6. mcp4_browser_evaluate → extract cookies, call save_session(portal, cookies) via sessions.py
```

Sessions are stored **encrypted** in `.sessions/{portal}.enc` using Fernet (AES-128-CBC + HMAC).
Plain `.sessions/*.json` files must never be written — always use `sessions.py`.

## Session Encryption

Session cookies are encrypted at rest using **Fernet** (symmetric AES-128-CBC + HMAC-SHA256).

### Setup (first run)
```bash
python3 sessions.py init    # generates SESSION_KEY in .env if missing
python3 sessions.py check   # verify key is valid
```

### Programmatic usage
```python
from sessions import ensure_key, save_session, load_session

ensure_key()                          # call once at startup
cookies = load_session('linkedin')    # returns list[dict] or None
save_session('linkedin', cookies)     # encrypts → .sessions/linkedin.enc
```

### File layout
- `.env` — contains `SESSION_KEY=<fernet-key>` (gitignored)
- `.env.example` — template showing required vars (tracked in git)
- `.sessions/*.enc` — encrypted cookie files (gitignored)
- **Never** write plain `.sessions/*.json` — always use `save_session()`

### Re-encrypt existing plain files
```bash
python3 sessions.py encrypt-all   # converts *.json → *.enc, removes plain files
```

## Credentials

**Passwords are never read from files** — the AI could read and leak them.

At startup, **ask the user in chat** for each site's password before opening any tabs. Passwords live only in the conversation context — never write them to a file or log them.

Prompt sequence (only ask for sites whose `.sessions/{portal}.enc` does not exist or fails to decrypt):
```
"Para comenzar necesito tus contraseñas. Escríbelas una por una:"
→ Trabajando.cl password:
→ Laborum.cl password:
→ GetOnBoard password:
→ CompuTrabajo password:
→ Indeed password:
```

- **LinkedIn and Google:** use OAuth sign-in with `{oauth_email from data/profile.tsv}` — no password prompt needed
- Valid `.sessions/{portal}.enc` files skip re-login until the session expires
- If `load_session(portal)` returns `None`, the session is missing/expired — prompt for login

## References

- `references/job-sites.md` — login flows, search selectors, and apply button locators per site
