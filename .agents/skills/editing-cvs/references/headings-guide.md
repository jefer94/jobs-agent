# Headings & Icons Guide

## Source of truth

Edit `data/headings.tsv` at the project root. Columns:

| Column | Purpose |
|--------|---------|
| `key` | Internal identifier used by the agent |
| `es` | Spanish section label (use this when offer is in Spanish) |
| `en` | English section label |
| `icon` | Unicode character prepended to section heading in PDF |
| `unicode` | Code point — search this on the reference sites below |

## Language rule

**Always match the language of the job offer.**  
If the offer is in Spanish → use the `es` column.  
If the offer is in English → use the `en` column.  
Never mix languages within a single CV.

## Icon reference (online)

Browse and copy icons from any of these:

| Site | Best for |
|------|----------|
| **https://symbl.cc/en/** | Search by name, preview, copy char |
| **https://unicode.org/charts/** | Official Unicode block charts (PDF) |
| **https://www.compart.com/en/unicode/** | Block browser + search |
| **https://www.fileformat.info/info/unicode/char/search.htm** | Code point lookup |

Recommended Unicode blocks for CV icons:
- **Geometric Shapes** U+25A0–U+25FF — ◆ ◈ ◎ ◉ ◇ ◫
- **Miscellaneous Symbols** U+2600–U+26FF — ☎ ✉ ✦
- **Mathematical Operators** U+2200–U+22FF — ⊕ ⊛
- **Box Drawing / Blocks** U+2500–U+257F — for subtle separators

## Current icon assignments

| Section key | Icon | Char |
|-------------|------|------|
| resumen | ◇ | U+25C7 |
| experiencia | ◈ | U+25C8 |
| educacion | ◎ | U+25CE |
| habilidades | ◆ | U+25C6 |
| proyectos | ◉ | U+25C9 |
| idiomas | ◫ | U+25EB |
| certificaciones | ✦ | U+2726 |
| contact email | ✉ | U+2709 |
| contact phone | ☎ | U+260E |
| contact github | ⊛ | U+229B |
| contact website | ⊕ | U+2295 |

## Choosing a new icon

1. Go to https://symbl.cc/en/ → search for a keyword (e.g. "star", "circle", "diamond")
2. Confirm it renders in **DejaVu Sans** (the PDF font) — preview the char in your terminal: `echo "◈"` 
3. Add it to `data/headings.tsv` in the `icon` column
4. The PDF converter will pick it up automatically on next render
