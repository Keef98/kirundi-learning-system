# Kirundi Language Learning System

A Kirundi-first AI-assisted language learning app for English/French speakers, focused on teaching practical spoken Kirundi in real-life situations.

## Quick start

1. Read `docs/PROJECT_BRIEF.md` — the full project brief
2. Read `docs/LABEL_GUIDE.md` — definitions for difficulty, register, review status
3. Read `docs/REVIEW_GUIDELINES.md` — how to review and approve content
4. Pick a situation folder in `data/pedagogical/` (start with `greetings/`)
5. Read the situation `README.md`, then start filling CSVs

## Project structure

```
docs/           → Project brief, guidelines, label definitions
data/raw/       → Raw Kirundi text for future pretraining
data/pedagogical/ → Teaching content organized by situation (YOUR MAIN WORK)
data/evaluation/  → Gold evaluation set
data/exports/     → Generated training data (do not edit manually)
scripts/        → Validation, export, and stats tools
prompts/        → System prompts for the retrieval prototype
config/         → Schema version tracking
```

## Content workflow

1. **Create** → Fill CSV files in a situation folder (set status to `draft`)
2. **Review** → Check each record against review guidelines (set to `reviewed`)
3. **Approve** → Confirm ready for production (set to `approved`)
4. **Export** → Run `scripts/export_training_data.py` to generate training triples

## Key principles

- **Kirundi-first**: write natural Kirundi, then add translations. Never translate from English.
- **Content before model**: curated content is the foundation. Model training comes later.
- **Situation-first**: organize everything around real speaking situations, not grammar.
- **Only approved content ships**: `draft` and `reviewed` records are work-in-progress only.
- **Watch for Kinyarwanda leakage**: flag it explicitly during review.

## Current status

- [ ] Greetings situation pack
- [ ] Market situation pack
- [ ] Family visit situation pack
- [ ] Gold evaluation set (30+ items)
- [ ] Validation script working
- [ ] Export script working
- [ ] Retrieval prototype
