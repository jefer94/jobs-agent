# Agent Skills Guide — Jobs Bot

Personal job-search automation bot for the Chilean market. This agent controls Chrome to find and apply to Spanish-language job offers in Chile, tailors CVs per application, and tracks performance over time.

**Hard constraint: never apply to an offer not written entirely in Spanish.**

---

## Project Overview

This is a single-user automation bot (not a product). It:

1. Browses Chilean job portals via Playwright-controlled Chrome
2. Reads the base CV from `docs/Espanol.pdf` and generates tailored versions per offer
3. Automates form filling and job submissions
4. Logs every application, records form Q&A, and tracks response/interview rates

**Stack:** Python · Playwright (chromium, headed) · pdfplumber / pypdf · JSON flat-file storage

---

## Project Structure

```
docs/               — Base CV (Espanol.pdf) and title certificate (titulo.pdf)
generated-cvs/      — Tailored CVs per application ({empresa}-{cargo}-{date}.md)
data/               — applications.json · qa-log.json · metrics.json
.sessions/          — Saved browser session cookies (gitignored)
.env                — Job site credentials (never commit)
```

---

## Setup

```bash
pip install playwright pdfplumber pypdf langdetect reportlab
playwright install chromium
```

Create `.env` with credentials for each site:
```
LINKEDIN_EMAIL=
LINKEDIN_PASSWORD=
TRABAJANDO_EMAIL=
TRABAJANDO_PASSWORD=
LABORUM_EMAIL=
LABORUM_PASSWORD=
```

Initialize data folder on first run — the `tracking-applications` skill includes a bootstrap script.

---

## Standard Workflow

Every job application follows this sequence:

```
1. browsing-job-sites  →  find relevant Spanish offers on Chilean portals
2. tracking-applications  →  check for duplicates before proceeding
3. editing-cvs + pdf  →  extract base CV, tailor for the specific offer
4. browsing-job-sites  →  fill and submit the application form
5. tracking-applications  →  log the application and any form Q&A
```

---

## Key Rules

- **Spanish only** — skip any offer whose description contains English paragraphs
- **No duplicates** — always query `data/applications.json` by URL before applying
- **No invented experience** — CV tailoring only reorders and emphasizes truthfully
- **Headed browser** — always `headless=False` so the user can observe and intervene
- **CAPTCHA** — stop, surface the page to the user, and wait for manual resolution
- **Credentials** — read exclusively from `.env`; never hardcode

---

## Available Skills

### pdf
**Source:** `anthropics/skills` · 56.5K installs

**Activate when:** reading, extracting, merging, or creating any `.pdf` file — including `docs/Espanol.pdf` and `docs/titulo.pdf`.

**Key tools:** `pdfplumber` for text/table extraction, `pypdf` for merge/split/rotate, `reportlab` for creating new PDFs, `pytesseract` for scanned OCR.

---

### browsing-job-sites
**Source:** custom (`.agents/skills/browsing-job-sites/`)

**Activate when:** user asks to search for jobs, browse a job site, log in, or submit an application.

**Covers:** LinkedIn · Trabajando.cl · Laborum.cl · GetOnBoard · CompuTrabajo · Indeed Chile · Google Jobs. See `references/job-sites.md` for selectors and login flows per site.

---

### editing-cvs
**Source:** custom (`.agents/skills/editing-cvs/`)

**Activate when:** a job offer needs a tailored CV, or user asks to generate or adapt the CV for a specific role.

**Output:** `generated-cvs/{empresa}-{cargo}-{YYYY-MM-DD}.md`. Uses the `pdf` skill to extract text from `docs/Espanol.pdf`. See `references/cv-guidelines.md` for Chilean CV structure and keyword-matching strategy.

---

### tracking-applications
**Source:** custom (`.agents/skills/tracking-applications/`)

**Activate when:** logging a new application, recording form Q&A, checking for duplicates, or reporting performance metrics.

**Storage:** `data/applications.json` (log) · `data/qa-log.json` (form answers) · `data/metrics.json` (response rate, interview rate, by-site breakdown). See `references/metrics-guide.md` for metric definitions and display format.

---

### create-skill
**Source:** `siviter-xyz/dot-agent`

**Activate when:** user asks to create or update a skill, or a repeated workflow should be captured as a reusable package.

**Rules:** `SKILL.md` must be under 200 lines; use gerund naming (`browsing-job-sites`); description must be in third person. After creating a skill, add it to this file.

---

### find-skills
**Source:** `vercel-labs/skills`

**Activate when:** a needed capability is not covered by the skills above, or user asks to extend the bot.

**Commands:** `npx skills find [query]` · `npx skills add <owner/repo@skill>` · `npx skills check`.
Only recommend skills with 1K+ installs and a reputable source.

---

## Adding New Skills

```bash
npx skills add <owner/repo@skill>
```

After installation, add a section under **Available Skills** above documenting the source, activation trigger, and key capabilities.
