#!/usr/bin/env python3
"""Print content statistics across all situations and content types."""

import csv
from pathlib import Path
from collections import Counter

DATA_DIR = Path(__file__).parent.parent / "data" / "pedagogical"
EVAL_DIR = Path(__file__).parent.parent / "data" / "evaluation"

FILE_TYPES = ["translations", "explanations", "corrections", "dialogues", "variants"]


def count_records(filepath: Path) -> dict:
    """Count records by review_status."""
    counts = Counter()
    if not filepath.exists():
        return counts
    with open(filepath, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            # Skip empty template rows
            ki = row.get("kirundi") or row.get("corrected_kirundi") or row.get("learner_input") or ""
            if not ki.strip():
                continue
            status = row.get("review_status", "draft")
            counts[status] += 1
    return counts


def main():
    situations = sorted([d for d in DATA_DIR.iterdir() if d.is_dir()])

    if not situations:
        print("No situation folders found.")
        return

    grand_total = Counter()
    grand_approved = 0

    print("=" * 60)
    print("KIRUNDI LEARNING SYSTEM — CONTENT STATISTICS")
    print("=" * 60)

    for situation_dir in situations:
        print(f"\n📁 {situation_dir.name}")
        print("-" * 40)
        situation_total = 0
        situation_approved = 0

        for file_type in FILE_TYPES:
            filepath = situation_dir / f"{file_type}.csv"
            counts = count_records(filepath)
            total = sum(counts.values())
            approved = counts.get("approved", 0)
            situation_total += total
            situation_approved += approved

            if total > 0:
                status_str = ", ".join(f"{k}: {v}" for k, v in sorted(counts.items()))
                print(f"  {file_type:15s}  {total:4d} records  ({status_str})")
            else:
                print(f"  {file_type:15s}     0 records")

        print(f"  {'TOTAL':15s}  {situation_total:4d} records  ({situation_approved} approved)")
        grand_total["all"] += situation_total
        grand_approved += situation_approved

    # Evaluation set
    eval_file = EVAL_DIR / "gold_eval.csv"
    eval_count = 0
    if eval_file.exists():
        with open(eval_file, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("prompt", "").strip():
                    eval_count += 1

    print(f"\n{'=' * 60}")
    print(f"GRAND TOTAL: {grand_total['all']} records ({grand_approved} approved)")
    print(f"EVALUATION SET: {eval_count} items")
    print(f"{'=' * 60}")

    # Milestone progress
    print(f"\n📊 MILESTONE PROGRESS")
    print(f"  M1 (greetings 50+ records):    {'✅' if grand_total.get('all', 0) >= 50 else '⬜'}")
    print(f"  M2 (3 situations, 150+ total): {'✅' if grand_total.get('all', 0) >= 150 else '⬜'}")
    print(f"  M3 (eval set 30+ items):       {'✅' if eval_count >= 30 else '⬜'}")
    print(f"  M4 (500+ approved records):    {'✅' if grand_approved >= 500 else '⬜'}")


if __name__ == "__main__":
    main()
