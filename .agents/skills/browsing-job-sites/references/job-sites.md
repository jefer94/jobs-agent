# Job Sites Reference

Login flows, search selectors, and apply patterns per site.

## LinkedIn

- **Login URL:** https://www.linkedin.com/login
- **OAuth:** Click "Iniciar sesión con Google" → sign in as `jdefreitaspinto@gmail.com`
- **Search URL:** https://www.linkedin.com/jobs/search/?keywords={query}&location=Chile&f_TPR=r604800
- **Language filter:** Add `&f_LL=es` for Spanish postings
- **Apply button:** `button[aria-label="Solicitar empleo"]` or `button[aria-label="Solicitud sencilla"]`
- **Easy Apply:** Prefer Easy Apply offers — look for `span:text("Solicitud sencilla")`
- **Session:** Save after OAuth to `.sessions/linkedin.json`
- **1 offer page rule:** Open offer, apply or skip, close tab — then open next

### LinkedIn Login Flow
```
1. Check .sessions/linkedin.json — if valid, skip login
2. Otherwise: navigate to login page
3. Click "Continuar con Google"
4. Select or type jdefreitaspinto@gmail.com
5. Complete Google OAuth flow
6. Save context storage state to .sessions/linkedin.json
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

- **Login URL:** https://www.trabajando.com/login
- **Search URL:** https://www.trabajando.com/trabajo-en/chile/?q={query}
- **Apply button:** `a.btn-postular` or `button:text("Postular")`
- **Notes:** Requires Chilean RUT for some offers — skip those if not available

---

## Laborum.cl

- **Login URL:** https://www.laborum.cl/login
- **Search URL:** https://www.laborum.cl/empleos?q={query}&l=Chile
- **Apply button:** `button:text("Postularme")` or `a:text("Postular")`
- **Notes:** Some offers redirect to company site — log URL and skip auto-apply

---

## GetOnBoard (getonbrd.com)

- **Login URL:** https://www.getonbrd.com/login
- **Search URL:** https://www.getonbrd.com/empleos?query={query}&country=CL
- **Apply button:** `a:text("Aplicar")` or `button:text("Aplicar a este trabajo")`
- **Language check:** Most offers are bilingual — only apply if description body is Spanish
- **Notes:** Tech-focused; best for developer/engineering roles

---

## CompuTrabajo Chile

- **Login URL:** https://cl.computrabajo.com/login
- **Search URL:** https://cl.computrabajo.com/trabajo-de-{query}
- **Apply button:** `a#applyBtn` or `button:text("Inscribirme")`

---

## Indeed Chile

- **Login URL:** https://secure.indeed.com/account/login
- **Search URL:** https://cl.indeed.com/jobs?q={query}&l=Chile&fromage=7
- **Apply button:** `button[aria-label="Postularse ahora"]` or `span:text("Postularse fácilmente")`
- **Language check:** Indeed mixes English/Spanish offers — verify `lang` attribute or scan first 100 chars of description

---

## Google Jobs

- **Search URL:** https://www.google.com/search?q={query}+trabajo+Chile&ibp=htl;jobs
- **Login:** Sign in to Google as `jdefreitaspinto@gmail.com` before searching (unlocks saved jobs and personalised results)
- **OAuth flow:** Navigate to accounts.google.com → sign in with `jdefreitaspinto@gmail.com` → save session to `.sessions/google.json`
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
