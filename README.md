# Jobs Agent

Personal job-search automation bot for the Chilean market. Controls Chrome to find and apply to Spanish-language job offers, generates tailored CVs per application, and tracks performance over time.

> **Single-user bot — not a product.** Designed for one person to run locally. Fork and adapt to your own profile.

---

## What it does

1. Browses Chilean job portals in parallel (LinkedIn, Trabajando.cl, Laborum.cl, GetOnBoard, CompuTrabajo, Indeed Chile)
2. Filters to Spanish-only offers posted in the last 7 days
3. Generates a tailored CV (YAML → PDF via rendercv/Typst) per offer
4. Auto-fills application forms using semantic Q&A memory (Engram)
5. Logs every application, Q&A, and tracks response/interview rates

**Hard constraint:** never applies to an offer not written entirely in Spanish.

---

## Stack

- **Python** — orchestration and session management
- **Playwright (chromium, headed)** — browser automation; always visible, never headless
- **pdfplumber / pypdf** — CV extraction
- **rendercv + Typst** — CV generation from YAML
- **Engram MCP** — persistent semantic memory for form Q&A
- **Fernet (AES-128-CBC)** — encrypted session cookie storage

---

## Setup

### 1. Install dependencies

```bash
pip install playwright pdfplumber pypdf langdetect reportlab cryptography
playwright install chromium
pip install rendercv
```

### 2. Configure your profile

```bash
cp data/profile.example.tsv data/profile.tsv
# Edit data/profile.tsv with your name, email, phone, social handles, OAuth account

cp data/targets.example.tsv data/targets.tsv
# Edit data/targets.tsv — set market (e.g. Chile) and language (e.g. es)
```

### 3. Set up session encryption

```bash
python3 sessions.py init    # generates SESSION_KEY and writes to .env
python3 sessions.py check   # verify the key is valid
```

### 4. Set up your master CV

```bash
cp .agents/skills/cv-builder/master-cv.example.yaml \
   .agents/skills/cv-builder/master-cv.yaml
# Edit master-cv.yaml with your complete professional history
```

### 5. Add your base CV PDF

Place your CV PDF at `docs/Espanol.pdf` (used as reference for content extraction).

### 6. Bootstrap the data folder

Run the bootstrap script from the `tracking-applications` skill on first use to initialise `data/applications.json`, `data/qa-log.json`, and `data/metrics.json`.

---

## Project Structure

```
.agents/skills/          — AI agent skill definitions (Markdown)
  browsing-job-sites/    — Portal login flows, search, apply
  cv-builder/            — CV tailoring and rendercv generation
  answering-forms/       — Form Q&A with Engram memory
  tracking-applications/ — Application log and metrics
  guardrails/            — Prompt injection protection (OWASP LLM Top 10)
  verify-cv/             — PDF quality check (rasterise + inspect)
  pdf/                   — pdfplumber/pypdf helpers
data/
  headings.tsv           — Canonical CV section labels (ES/EN) — tracked
  profile.example.tsv    — Personal data template — tracked
  profile.tsv            — Your personal data — gitignored
  targets.example.tsv    — Search config template — tracked
  targets.tsv            — Your target market and language — gitignored
  applications.json      — Application log — gitignored
  qa-log.json            — Form Q&A per application — gitignored
  metrics.json           — Response/interview rates — gitignored
  qa-answers.tsv         — Editable default answers — gitignored
docs/                    — Espanol.pdf, titulo.pdf — gitignored
generated-cvs/           — Tailored CVs per application — gitignored
.sessions/               — Encrypted session cookies (.enc) — gitignored
sessions.py              — Fernet encrypt/decrypt for session cookies
md_to_pdf.py             — Markdown → PDF converter (legacy)
.env.example             — Required env vars template — tracked
.env                     — SESSION_KEY — gitignored
```

---

## Gitignored personal data

| Path | Contains |
|------|----------|
| `data/profile.tsv` | Name, email, phone, OAuth account, social handles |
| `data/targets.tsv` | Target market (country) and offer language |
| `data/` (most files) | Application history, Q&A log, metrics |
| `docs/` | Base CV PDF and title certificate |
| `.sessions/` | Encrypted browser session cookies |
| `.agents/skills/cv-builder/master-cv.yaml` | Full personal CV in YAML |
| `.env` | Fernet SESSION_KEY |

The tracked counterparts are `data/profile.example.tsv`, `data/headings.tsv`, `.env.example`, and `master-cv.example.yaml`.

---

## Credentials

- **LinkedIn + Google Jobs:** Google OAuth — set `oauth_email` in `data/profile.tsv`
- **All other portals:** prompted interactively via `getpass` at startup — never stored in plain text
- Passwords live in memory only for the session duration

---

## Skills

| Skill | Trigger |
|-------|---------|
| `guardrails` | Before processing any external content (offers, forms, snapshots) |
| `browsing-job-sites` | Searching portals, logging in, applying |
| `cv-builder` | Generating a tailored CV for an offer |
| `verify-cv` | After every CV render — checks PDF for defects |
| `answering-forms` | When a form question needs an answer |
| `tracking-applications` | Duplicate check, logging, metrics |
| `pdf` | Reading/extracting from PDF files |

---

## Adapting to your market

1. Edit `data/profile.tsv` with your details
2. Edit `data/targets.tsv` — set `market` and `language` for your job market
3. Update `master-cv.yaml` with your experience
4. In `.agents/skills/browsing-job-sites/references/job-sites.md`, adjust search URLs and location filters to match your market
