# Training Data Exports

## Purpose

This folder contains generated training data in JSONL format. **Do not edit these files manually** — they are generated from the pedagogical CSVs by `scripts/export_training_data.py`.

## Files (generated)

- `training_all.jsonl` — all approved examples
- `training_translation.jsonl` — translation pairs only
- `training_explanation.jsonl` — explanation examples only
- `training_correction.jsonl` — correction examples only
- `training_dialogue.jsonl` — dialogue examples only
- `training_variants.jsonl` — variant examples only

## How to regenerate

```bash
python scripts/export_training_data.py
```

## Format

Each line is a JSON object:

```json
{"instruction": "...", "input": "...", "output": "..."}
```

See `docs/TRAINING_EXPORT_FORMAT.md` for full conversion rules.
