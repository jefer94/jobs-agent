---
name: tracking-applications
description: Stores job applications, records questions and answers from application forms, and measures bot performance (applications sent, responses received, interview rate). Use when logging a new application, recording form Q&A, checking application history, or reviewing performance metrics.
---

# Tracking Applications

Maintains a persistent log of all job applications, form questions and answers, and performance metrics. Storage is in `data/` as JSON files.

## When to Use

- A new job application has been submitted — log it
- A job application form asked questions — record Q&A
- User asks "how many jobs have I applied to?"
- User asks to see performance metrics or success rate
- Before applying: check if this offer was already applied to

## Storage Structure

```
data/
  applications.json   — list of all applications
  qa-log.json         — questions and answers per application
  metrics.json        — aggregated performance stats
```

## Application Record Schema

```json
{
  "id": "uuid",
  "date": "2024-01-15",
  "site": "linkedin",
  "company": "Empresa S.A.",
  "role": "Desarrollador Backend",
  "url": "https://...",
  "cv_used": "generated-cvs/empresa-dev-2024-01-15.md",
  "status": "applied | viewed | interview | rejected | offer | ignored",
  "notes": ""
}
```

## Q&A Record Schema

```json
{
  "application_id": "uuid",
  "question": "¿Cuál es tu pretensión de renta?",
  "answer": "Negociable según las responsabilidades del cargo",
  "date": "2024-01-15"
}
```

## Key Operations

**Log application:**
Load `data/applications.json`, append new record, save.

**Check for duplicate:**
Search `applications.json` by `url` or `(company + role)` before applying.

**Record Q&A:**
Append to `data/qa-log.json` with the `application_id` from the logged application.

**Update status:**
Find record by `id`, update `status` field.

## Metrics

Compute and update `data/metrics.json` after each operation:

```json
{
  "total_applied": 0,
  "viewed": 0,
  "interviews": 0,
  "rejected": 0,
  "offers": 0,
  "response_rate": 0.0,
  "interview_rate": 0.0,
  "by_site": {},
  "last_updated": "2024-01-15"
}
```

- `response_rate` = (viewed + interviews + rejected + offers) / total_applied
- `interview_rate` = interviews / total_applied

## References

- `references/metrics-guide.md` — how to interpret and display performance metrics
