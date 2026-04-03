# Training Export Format

## Purpose

This document defines how curated CSV content is converted into model training data. The export is **generated**, not manually maintained. Your source of truth is always the CSV files.

## Output format

Each training example is an instruction / input / output triple, exported as JSONL:

```json
{"instruction": "...", "input": "...", "output": "..."}
```

## Conversion rules by content type

### Translation pairs

**English → Kirundi:**
```json
{
  "instruction": "Translate the following English sentence to Kirundi.",
  "input": "Good morning, sir.",
  "output": "Mwaramutse, mushingantahe."
}
```

**French → Kirundi:**
```json
{
  "instruction": "Traduisez la phrase suivante en kirundi.",
  "input": "Bonjour, monsieur.",
  "output": "Mwaramutse, mushingantahe."
}
```

**Kirundi → English:**
```json
{
  "instruction": "Translate the following Kirundi sentence to English.",
  "input": "Mwaramutse, mushingantahe.",
  "output": "Good morning, sir."
}
```

**Kirundi → French:**
```json
{
  "instruction": "Traduisez la phrase suivante du kirundi en français.",
  "input": "Mwaramutse, mushingantahe.",
  "output": "Bonjour, monsieur."
}
```

One translation CSV row produces up to 4 training examples.

### Explanation examples

```json
{
  "instruction": "Explain the following Kirundi sentence simply in English.",
  "input": "Mwaramutse, mushingantahe.",
  "output": "This means 'good morning, sir.' The word 'mushingantahe' is a respectful way to address an older man."
}
```

French version also generated from the same row.

### Correction pairs

```json
{
  "instruction": "A learner of Kirundi wrote the following sentence. Correct it and explain what is wrong.",
  "input": "Mwaramutse, mzee.",
  "output": "The correct sentence is 'Mwaramutse, mushingantahe.' The word 'mzee' is Swahili, not Kirundi. Use 'mushingantahe' to respectfully address an older man."
}
```

### Dialogue (turn-by-turn)

For a dialogue with N turns, generate N-1 continuation examples:

```json
{
  "instruction": "Continue the following Kirundi dialogue. The setting is: greeting at the market.",
  "input": "A: Mwaramutse!\nB: Mwaramutse! Amakuru?",
  "output": "A: Ni meza, urakomeye?"
}
```

### Variant sets

```json
{
  "instruction": "Give 3 natural ways to greet an elder in Kirundi. Register: respectful.",
  "input": "Situation: greeting an elder",
  "output": "1. Mwaramutse, mushingantahe.\n2. Mushingantahe, mwaramutse. Amakuru?\n3. Mwaramutse, mugabo wacu."
}
```

## Export rules

- Only export records with `review_status = approved`
- Include situation and register metadata as context when helpful
- Vary instruction phrasing slightly across examples (the export script should have templates)
- Generate both English and French instruction variants where applicable

## File output

Exports go to `data/exports/` as JSONL files:
- `training_all.jsonl` — all approved examples
- `training_translation.jsonl` — translation examples only
- `training_explanation.jsonl` — explanation examples only
- `training_correction.jsonl` — correction examples only
- `training_dialogue.jsonl` — dialogue examples only
- `training_variants.jsonl` — variant examples only
