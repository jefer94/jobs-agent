---
name: answering-forms
description: Handles job application form questions by searching Engram memory for semantically similar past answers, falling back to CV-based generation. Stores all answers in data/qa-answers.tsv for manual editing. Use when a job application form shows a question that needs to be answered.
---

# Answering Forms

When a job application form presents a question, use Engram's semantic search to find a previously written answer, then save any new answers for reuse.

## When to Use

- An application form shows a question (salary expectation, availability, motivation, etc.)
- User asks to check what was answered for a question before
- User wants to review or update standard answers

## Answer Lookup Workflow

```
Task Progress:
- [ ] 1. Detect question text from the form (mcp4_browser_snapshot)
- [ ] 2. Search Engram for semantically similar past questions (mcp3_mem_search)
- [ ] 3. If match found (similarity looks close): use that answer
- [ ] 4. If no match: check data/qa-answers.tsv for fuzzy match on question column
- [ ] 5. If still no match: generate new answer from CV context + company/role
- [ ] 6. Type the answer into the form field (mcp4_browser_type or mcp4_browser_fill_form)
- [ ] 7. Save new Q&A to data/qa-answers.tsv and Engram memory
```

## Engram Search

Use `mcp3_mem_search` to find semantically similar questions:

- `query`: the exact question text from the form
- `project`: `jobs-bot`
- `type`: `manual`
- Pick the top result — if the title or content closely matches the question, use its answer

Save new answers with `mcp3_mem_save`:
- `title`: the question text (truncated to 80 chars)
- `content`: `**Answer**: {answer}\n**Context**: {role} at {company}`
- `project`: `jobs-bot`
- `type`: `manual`

## TSV Store

All answers are persisted in `data/qa-answers.tsv` (tab-separated, UTF-8). This file is the **editable source of truth** — the user can open it and change answers at any time.

### Columns
```
question	answer	context	updated
```

- **question** — full question text as it appeared on the form
- **answer** — the answer given
- **context** — optional: role or site where this was asked
- **updated** — ISO date of last edit (YYYY-MM-DD)

### Reading the TSV
```python
import csv

def load_answers(path="data/qa-answers.tsv") -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))
```

### Appending a new answer
```python
def save_answer(question, answer, context="", path="data/qa-answers.tsv"):
    from datetime import date
    import csv, os
    write_header = not os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        if write_header:
            w.writerow(["question", "answer", "context", "updated"])
        w.writerow([question, answer, context, date.today().isoformat()])
```

## Common Questions & Suggested Answers

Pre-seed `data/qa-answers.tsv` with these on first run:

| Question | Suggested default |
|---|---|
| ¿Cuál es tu pretensión de renta? | Negociable según responsabilidades |
| ¿Tienes disponibilidad inmediata? | Sí, disponibilidad inmediata |
| ¿Modalidad de trabajo preferida? | Híbrido o remoto |
| ¿Por qué te interesa este cargo? | Generate per offer using company + role |
| ¿Nivel de inglés? | Read from docs/Espanol.pdf |
| ¿Tienes vehículo propio? | No |
| ¿Estás dispuesto a viajar? | Ocasionalmente |
