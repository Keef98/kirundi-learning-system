# Raw Kirundi Corpus

## Purpose

Store raw Kirundi text that is **not** structured for teaching. This is for future use in continued pretraining / language adaptation.

## What goes here

- Natural Kirundi text from any source
- Dialogues, stories, informational text, conversations
- Unstructured — no need for situation tags or translations

## Format

Plain text files (`.txt`) or CSVs with minimal metadata:

```
id,text,source_type,source_url,license,language_confidence,notes
```

## When to start collecting

Not urgent for v1. Focus on pedagogical content first. Start collecting raw text when you're preparing for model fine-tuning (Phase 2+).

## Quality bar

- Must be Kirundi (not Kinyarwanda)
- Source should be documented
- License should be noted if from a published source
