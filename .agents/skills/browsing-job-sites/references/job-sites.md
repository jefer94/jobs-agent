# Job Sites Reference

Login flows, search selectors, and apply patterns per site.

## LinkedIn

- **Login URL:** https://www.linkedin.com/login
- **OAuth:** Click "Iniciar sesión con Google" → sign in as `{oauth_email from data/profile.tsv}`
- **Search URL:** https://www.linkedin.com/jobs/search/?keywords={query}&geoId=104621616&f_TPR=r86400&f_WT=1%2C2%2C3
  - `geoId=104621616` → Santiago de Chile
  - `f_TPR=r86400` → last 24 h (use `r604800` for last week)
  - `f_WT=1%2C2%2C3` → on-site + remote + hybrid
- **Language filter:** Add `&f_LL=es` for Spanish postings
- **Apply button:** `button[aria-label="Solicitar empleo"]` or `button[aria-label="Solicitud sencilla"]`
- **Easy Apply:** Prefer Easy Apply offers — look for `span:text("Solicitud sencilla")`
- **Session:** Save after OAuth to `.sessions/linkedin.enc`
- **1 offer page rule:** Open offer, apply or skip, close tab — then open next

### LinkedIn Login Flow
```
1. Check .sessions/linkedin.enc — if valid, skip login
2. Otherwise: navigate to login page
3. Click "Continuar con Google"
4. Select or type `{oauth_email from data/profile.tsv}`
5. Complete Google OAuth flow
6. Save context storage state to .sessions/linkedin.enc (via sessions.py)
```

### LinkedIn Search Flow
```
1. Navigate to search URL with keywords from CV
2. Filter: Date posted → Last week
3. Filter: Language → Spanish (if available)
4. For each card: check title + description language before clicking
5. Open offer → apply → close page → wait 3–5s → next offer
```

---

## Trabajando.cl

- **Login URL:** https://www.trabajando.cl/login
- **Search URL:** https://www.trabajando.cl/trabajo-empleo/{query}?ubicacion=metropolitana+de+santiago&region=1
  - Replace spaces in query with `%20` (e.g. `solution%20architect`)
- **Apply button:** `a.btn-postular` or `button:text("Postular")`
- **Session:** `.sessions/trabajando.enc`
- **Notes:** Requires Chilean RUT for some offers — skip those if not available

---

## Laborum.cl

- **Login URL:** https://www.laborum.cl/login
- **Search URL:** https://www.laborum.cl/en-region-metropolitana/empleos-busqueda-{query}.html
  - Replace spaces with `-` (e.g. `arquitecto-de-soluciones`)
- **Apply button:** `button:text("Postularme")` or `a:text("Postular")`
- **Session:** `.sessions/laborum.enc`
- **Notes:** Some offers redirect to company site — log URL and skip auto-apply

---

## GetOnBoard (getonbrd.com)

- **Login URL:** https://www.getonbrd.com/login
- **Search URL:** https://www.getonbrd.com/jobs-{query}
  - Replace spaces with `-` (e.g. `jobs-solution-architect`)
- **My Jobs (saved/applied):** https://www.getonbrd.com/myjobs
- **Apply button:** `a:text("Aplicar")` or `button:text("Aplicar a este trabajo")`
- **Language check:** Most offers are bilingual — only apply if description body is Spanish
- **Session:** `.sessions/getonbrd.enc`
- **Notes:** Tech-focused; best for developer/engineering roles

---

## CompuTrabajo Chile

- **Login URL:** https://cl.computrabajo.com/login
- **Search URL:** https://cl.computrabajo.com/trabajo-de-{query}
  - Replace spaces with `-` (e.g. `trabajo-de-arquitecto-de-soluciones`)
- **Apply button:** `a#applyBtn` or `button:text("Inscribirme")`
- **Session:** `.sessions/computrabajo.enc`

---

## Indeed Chile

- **Login URL:** https://secure.indeed.com/account/login
- **Search URL:** https://cl.indeed.com/jobs?q={query}&l=Santiago+de+Chile%2C+Regi%C3%B3n+Metropolitana
  - Optionally append `&fromage=1` (last 24h) or `&fromage=7` (last week)
- **Apply button:** `button[aria-label="Postularse ahora"]` or `span:text("Postularse fácilmente")`
- **Session:** `.sessions/indeed.enc`
- **Language check:** Indeed mixes English/Spanish offers — verify `lang` attribute or scan first 100 chars of description

---

## Google Jobs

- **Search URL:** https://www.google.com/search?q={query}+trabajo+Chile&ibp=htl;jobs
- **Login:** Sign in to Google as `{oauth_email from data/profile.tsv}` before searching (unlocks saved jobs and personalised results)
- **OAuth flow:** Navigate to accounts.google.com → sign in with `{oauth_email from data/profile.tsv}` → save session to `.sessions/google.enc` (via sessions.py)
- Scrape job cards from Google's jobs panel
- Each card links to the original site — follow link and apply there
- **Selector:** `div[data-ved] .BjJfJf` for job titles in the panel
- **1 offer page rule:** Follow external link, apply or skip, close tab — then next card

---

## Language Detection

To verify an offer is in Spanish, check the first 200 characters of the job description:

```python
import langdetect

def is_spanish(text: str) -> bool:
    try:
        return langdetect.detect(text[:500]) == "es"
    except Exception:
        return False
```

Install: `pip install langdetect`

---

## Common Anti-Bot Measures

- **1 offer page per portal:** Never open more than 1 job offer detail page per portal context simultaneously
- **Rate limiting:** Add `page.wait_for_timeout(2000)` between actions; 3–5s between offer pages
- **CAPTCHA:** If `iframe[src*="recaptcha"]` appears, pause and alert user
- **IP blocks:** Use residential proxy or slow down if blocked (429 responses)
- **Realistic pacing:** Vary wait times slightly using `random.uniform(2, 5)` to avoid fixed-interval detection
