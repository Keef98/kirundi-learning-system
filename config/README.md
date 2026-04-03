# Config

## Schema versioning

`schema_version.json` tracks the current schema version and changelog. When you add or rename CSV columns, update the version here.

## Principle

- Prefer additive changes (add columns, don't rename or remove)
- Document every change
- Test on a few records before applying to the full dataset
