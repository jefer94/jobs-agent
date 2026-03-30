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
data/               — applications.json · qa-log.json · metrics.json · qa-answers.tsv
.sessions/          — Saved browser session cookies per portal (gitignored)
```

---

## Setup

```bash
pip install playwright pdfplumber pypdf langdetect reportlab
playwright install chromium
```

**No credentials file.** At startup the bot prompts for site passwords interactively via `getpass` — passwords live in memory only for the session and are never written to disk.

- **LinkedIn + Google Jobs:** sign in via Google OAuth as `jdefreitaspinto@gmail.com` — no password prompt
- **All other sites:** asked in chat once at startup; skipped if `.sessions/{portal}.json` is still valid

Initialize data folder on first run — the `tracking-applications` skill includes a bootstrap script.

---

## Standard Workflow

Every job application follows this sequence:

```
1. browsing-job-sites  →  prompt credentials at startup (once per session)
2. browsing-job-sites  →  open one browser context per portal, all in parallel
3. browsing-job-sites  →  search all portals simultaneously for Spanish offers
4. tracking-applications  →  check for duplicates before proceeding on each offer
5. editing-cvs + pdf  →  extract base CV, tailor for the specific offer
6. browsing-job-sites  →  open offer page (max 1 per portal), apply, close page
7. answering-forms      →  for each form question: search Engram, use TSV answer or generate new one
8. tracking-applications  →  log the application and any form Q&A
```

---

## Key Rules

- **Spanish only** — skip any offer whose description contains English paragraphs
- **No duplicates** — always query `data/applications.json` by URL before applying
- **No invented experience** — CV tailoring only reorders and emphasizes truthfully
- **Headed browser** — always `headless=False` so the user can observe and intervene
- **CAPTCHA** — stop, surface the page to the user, and wait for manual resolution
- **Credentials** — prompted interactively at startup via `getpass`; never read from files, never hardcoded; AI must not store or log passwords
- **OAuth** — LinkedIn and Google sign-in use Google OAuth with `jdefreitaspinto@gmail.com`
- **Parallel portals** — one browser context per portal, all running simultaneously
- **1 offer page per portal** — open, apply/skip, close before opening the next — reduces bot detection risk

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

### answering-forms
**Source:** custom (`.agents/skills/answering-forms/`)

**Activate when:** a job application form presents a question that needs an answer.

**How it works:** Searches Engram (`mcp3_mem_search`) for semantically similar past questions first. Falls back to `data/qa-answers.tsv` for a direct match, then generates a new answer from CV context. Saves every new Q&A to both the TSV (editable by user) and Engram memory (for future semantic matching).

**TSV:** `data/qa-answers.tsv` — tab-separated columns: `question · answer · context · updated`. Edit this file to change default answers at any time.

---

### tracking-applications
**Source:** custom (`.agents/skills/tracking-applications/`)

**Activate when:** logging a new application, recording form Q&A, checking for duplicates, or reporting performance metrics.

**Storage:** `data/applications.json` (log) · `data/qa-log.json` (form answers) · `data/metrics.json` (response rate, interview rate, by-site breakdown). See `references/metrics-guide.md` for metric definitions and display format.

---

### verify-cv
**Source:** custom (`.agents/skills/verify-cv/`)

**Activate when:** immediately after any CV PDF is generated (editing-cvs, cv-builder, or pdf skill). Always run before logging an application.

**How it works:** Opens the PDF via `mcp4_browser_navigate file:///<path>`, screenshots each page with `mcp4_browser_take_screenshot`, and visually inspects for: text overlap, clipping, multi-page overflow, missing sections, Unicode encoding boxes. Applies targeted fixes and re-renders if issues are found.

**Reports:** `✅ PASS` / `⚠️ FIXED` / `❌ FAIL` per CV file.

---

### cv-builder
**Source:** `claude-office-skills/skills` · installed via `npx skills add`

**Activate when:** user asks to generate a professionally formatted CV/resume as a PDF, or needs a structured YAML-driven CV with multiple themes.

**How it works:** Define CV content as a `rendercv` YAML file, then render to PDF with `rendercv render cv.yaml`. Output goes to `rendercv_output/`. Available themes: `classic`, `sb2nov`, `moderncv`, `engineeringresumes`.

**Output:** `generated-cvs/{empresa}-{cargo}-{YYYY-MM-DD}.yaml` → rendered to PDF via `rendercv`.

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
