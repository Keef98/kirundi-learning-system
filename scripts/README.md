# Scripts

## Available scripts

### `validate_csv.py`
Validates all CSV files against the expected schema. Checks for:
- Required columns present
- Valid label values (difficulty, register, review_status, source_type)
- No empty Kirundi fields in non-draft records
- ID uniqueness
- Consistent situation tags

Usage:
```bash
python scripts/validate_csv.py
```

Tests (from repo root): `python -m unittest discover -s tests -v`

### `export_training_data.py`
Converts approved CSV records into instruction/input/output JSONL files for model training. See `docs/TRAINING_EXPORT_FORMAT.md` for conversion rules.

Usage:
```bash
python scripts/export_training_data.py
```

### `stats.py`
Prints content statistics: records per situation, per type, per status, per difficulty. Helps you track coverage and progress toward milestones.

Usage:
```bash
python scripts/stats.py
```
