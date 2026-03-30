# Metrics Guide

How to interpret, display, and update performance metrics for the job application bot.

## Metrics Definitions

| Metric | Formula | Good benchmark |
|---|---|---|
| `response_rate` | (viewed + interviews + rejected + offers) / total_applied | > 15% |
| `interview_rate` | interviews / total_applied | > 5% |
| `offer_rate` | offers / total_applied | > 1% |
| `avg_days_to_response` | mean(response_date - apply_date) | < 14 days |

## Status Flow

```
applied → viewed → interview → offer
       ↘ rejected
       ↘ ignored (no response after 30 days)
```

Update status when:
- **viewed**: site shows "vista" / "seen" on application
- **interview**: recruiter contact received (log in notes)
- **rejected**: formal rejection received
- **offer**: offer received (update notes with details)
- **ignored**: auto-update after 30 days with no change

## Displaying Metrics

When user asks for a performance report, format as:

```
📊 Resumen de postulaciones

Total postuladas:    {total_applied}
Vistas:              {viewed} ({viewed/total*100:.0f}%)
Entrevistas:         {interviews} ({interview_rate*100:.1f}%)
Rechazos:            {rejected}
Ofertas:             {offers}

Tasa de respuesta:   {response_rate*100:.1f}%
Tasa de entrevistas: {interview_rate*100:.1f}%

Por sitio:
  LinkedIn:          {by_site.linkedin}
  Trabajando.cl:     {by_site.trabajando}
  Laborum.cl:        {by_site.laborum}
  GetOnBoard:        {by_site.getonbrd}
  Indeed Chile:      {by_site.indeed}

Última actualización: {last_updated}
```

## Common Q&A Patterns

Recurring questions in Chilean job application forms. Suggested answers to reuse:

| Question | Suggested Answer |
|---|---|
| ¿Pretensión de renta? | "Negociable según las responsabilidades" or specific amount |
| ¿Disponibilidad? | "Inmediata" or "15 días" |
| ¿Modalidad preferida? | "Híbrido o remoto" |
| ¿Por qué te interesa la empresa? | Generate per company from company website |
| ¿Nivel de inglés? | Read from CV docs/Espanol.pdf |
| ¿Tienes experiencia con X? | Cross-reference with CV skills |

Reuse answers from `data/qa-log.json` when the same question appears again — search by `question` field (fuzzy match on first 40 chars).

## Data Initialization

If `data/` files do not exist, create them:

```python
import json, os

os.makedirs("data", exist_ok=True)

defaults = {
    "applications.json": [],
    "qa-log.json": [],
    "metrics.json": {
        "total_applied": 0, "viewed": 0, "interviews": 0,
        "rejected": 0, "offers": 0, "response_rate": 0.0,
        "interview_rate": 0.0, "by_site": {}, "last_updated": ""
    }
}

for filename, default in defaults.items():
    path = f"data/{filename}"
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(default, f, indent=2, ensure_ascii=False)
```
