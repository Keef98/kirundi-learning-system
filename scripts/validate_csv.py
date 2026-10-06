#!/usr/bin/env python3
"""Validate all pedagogical CSV files against the expected schema."""

import csv
import sys
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "pedagogical"

VALID_DIFFICULTY = {"beginner", "elementary", "intermediate", ""}
VALID_REGISTER = {"neutral", "polite", "respectful", "informal", "child_friendly", "formal", ""}
VALID_REVIEW_STATUS = {"draft", "reviewed", "approved", ""}
VALID_SOURCE_TYPE = {"original", "collected", "adapted", ""}

EXPECTED_COLUMNS = {
    "translations": ["id", "situation", "kirundi", "translation_en", "translation_fr", "difficulty", "register", "speaker_context", "source_type", "review_status", "notes"],
    "explanations": ["id", "situation", "kirundi", "explanation_en", "explanation_fr", "difficulty", "register", "source_type", "review_status", "notes"],
    "corrections": ["id", "situation", "learner_input", "corrected_kirundi", "error_type", "explanation_en", "explanation_fr", "difficulty", "register", "source_type", "review_status", "notes"],
    "dialogues": ["dialogue_id", "situation", "title", "turn_number", "speaker_role", "kirundi", "translation_en", "translation_fr", "difficulty", "register", "source_type", "review_status", "notes"],
    "variants": ["id", "situation", "intent", "variant_number", "kirundi", "translation_en", "translation_fr", "difficulty", "register", "source_type", "review_status", "notes"],
}

def validate_file(filepath: Path, file_type: str, situation_folder: str) -> list[str]:
    errors = []
    expected = EXPECTED_COLUMNS.get(file_type)
    if not expected:
        errors.append(f"  Unknown file type: {file_type}")
        return errors

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        actual_cols = reader.fieldnames or []

        # Check columns
        missing = set(expected) - set(actual_cols)
        extra = set(actual_cols) - set(expected)
        if missing:
            errors.append(f"  Missing columns: {missing}")
        if extra:
            errors.append(f"  Unexpected columns: {extra}")

        keys_seen = set()
        for i, row in enumerate(reader, start=2):
            row_id = (row.get("id") or row.get("dialogue_id") or "").strip()

            # Check for duplicate IDs (skip empty placeholder rows)
            if row_id:
                if file_type == "dialogues":
                    turn = (row.get("turn_number") or "").strip()
                    key = (row_id, turn)
                    if key in keys_seen:
                        errors.append(
                            f"  Row {i}: duplicate dialogue_id '{row_id}' with turn_number '{turn}'"
                        )
                    else:
                        keys_seen.add(key)
                elif file_type == "variants":
                    variant = (row.get("variant_number") or "").strip()
                    key = (row_id, variant)
                    if key in keys_seen:
                        errors.append(
                            f"  Row {i}: duplicate id '{row_id}' with variant_number '{variant}'"
                        )
                    else:
                        keys_seen.add(key)
                else:
                    if row_id in keys_seen:
                        errors.append(f"  Row {i}: duplicate id '{row_id}'")
                    else:
                        keys_seen.add(row_id)

            situation = (row.get("situation") or "").strip()
            if situation != situation_folder:
                errors.append(
                    f"  Row {i}: situation '{situation}' does not match folder '{situation_folder}'"
                )

            # Validate label values
            difficulty = row.get("difficulty", "")
            if difficulty and difficulty not in VALID_DIFFICULTY:
                errors.append(f"  Row {i}: invalid difficulty '{difficulty}'")

            register = row.get("register", "")
            if register and register not in VALID_REGISTER:
                errors.append(f"  Row {i}: invalid register '{register}'")

            status = row.get("review_status", "")
            if status and status not in VALID_REVIEW_STATUS:
                errors.append(f"  Row {i}: invalid review_status '{status}'")

            source = row.get("source_type", "")
            if source and source not in VALID_SOURCE_TYPE:
                errors.append(f"  Row {i}: invalid source_type '{source}'")

            # Check that non-draft records have kirundi filled
            kirundi = row.get("kirundi") or row.get("corrected_kirundi") or ""
            if status in ("reviewed", "approved") and not kirundi.strip():
                errors.append(f"  Row {i}: status is '{status}' but kirundi field is empty")

    return errors


def main():
    total_errors = 0
    situations = [d for d in DATA_DIR.iterdir() if d.is_dir()]

    if not situations:
        print("No situation folders found in data/pedagogical/")
        sys.exit(1)

    for situation_dir in sorted(situations):
        print(f"\n📁 {situation_dir.name}/")
        for csv_file in sorted(situation_dir.glob("*.csv")):
            file_type = csv_file.stem
            errors = validate_file(csv_file, file_type, situation_dir.name)
            if errors:
                print(f"  ❌ {csv_file.name}")
                for e in errors:
                    print(f"    {e}")
                total_errors += len(errors)
            else:
                print(f"  ✅ {csv_file.name}")

    # Also validate evaluation set
    eval_file = Path(__file__).parent.parent / "data" / "evaluation" / "gold_eval.csv"
    if eval_file.exists():
        print(f"\n📁 evaluation/")
        print(f"  ✅ gold_eval.csv (schema validation not yet implemented for eval)")

    print(f"\n{'='*40}")
    if total_errors == 0:
        print("All files valid! ✅")
    else:
        print(f"{total_errors} error(s) found. ❌")
        sys.exit(1)


if __name__ == "__main__":
    main()
