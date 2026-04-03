#!/usr/bin/env python3
"""Export approved CSV records into instruction/input/output JSONL for training."""

import csv
import json
import random
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "pedagogical"
EXPORT_DIR = Path(__file__).parent.parent / "data" / "exports"

# Instruction templates (varied phrasing for robustness)
TRANSLATE_EN_TO_KI = [
    "Translate the following English sentence to Kirundi.",
    "How would you say this in Kirundi?",
    "Give the Kirundi translation of this English sentence.",
]
TRANSLATE_FR_TO_KI = [
    "Traduisez la phrase suivante en kirundi.",
    "Comment dit-on cela en kirundi ?",
    "Donnez la traduction en kirundi de cette phrase française.",
]
TRANSLATE_KI_TO_EN = [
    "Translate the following Kirundi sentence to English.",
    "What does this Kirundi sentence mean in English?",
]
TRANSLATE_KI_TO_FR = [
    "Traduisez la phrase suivante du kirundi en français.",
    "Que signifie cette phrase en kirundi ? Répondez en français.",
]
EXPLAIN_EN = [
    "Explain the following Kirundi sentence simply in English.",
    "What does this Kirundi sentence mean? Explain simply in English.",
]
EXPLAIN_FR = [
    "Expliquez la phrase kirundi suivante simplement en français.",
    "Que signifie cette phrase en kirundi ? Expliquez simplement en français.",
]
CORRECT = [
    "A learner of Kirundi wrote the following sentence. Correct it and explain what is wrong.",
    "This Kirundi sentence has an error. Fix it and explain the mistake simply.",
]
DIALOGUE_CONTINUE = [
    "Continue the following Kirundi dialogue naturally.",
    "What would the next speaker say in this Kirundi conversation?",
]
GENERATE_VARIANTS = [
    "Give {n} natural ways to say this in Kirundi.",
    "Provide {n} different Kirundi expressions for this situation.",
]


def pick(templates: list[str], **kwargs) -> str:
    t = random.choice(templates)
    return t.format(**kwargs) if kwargs else t


def export_translations(situation_dir: Path) -> list[dict]:
    examples = []
    filepath = situation_dir / "translations.csv"
    if not filepath.exists():
        return examples

    with open(filepath, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("review_status") != "approved":
                continue
            ki = row["kirundi"].strip()
            en = row.get("translation_en", "").strip()
            fr = row.get("translation_fr", "").strip()
            if not ki:
                continue

            if en:
                examples.append({"instruction": pick(TRANSLATE_EN_TO_KI), "input": en, "output": ki})
                examples.append({"instruction": pick(TRANSLATE_KI_TO_EN), "input": ki, "output": en})
            if fr:
                examples.append({"instruction": pick(TRANSLATE_FR_TO_KI), "input": fr, "output": ki})
                examples.append({"instruction": pick(TRANSLATE_KI_TO_FR), "input": ki, "output": fr})

    return examples


def export_explanations(situation_dir: Path) -> list[dict]:
    examples = []
    filepath = situation_dir / "explanations.csv"
    if not filepath.exists():
        return examples

    with open(filepath, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("review_status") != "approved":
                continue
            ki = row["kirundi"].strip()
            ex_en = row.get("explanation_en", "").strip()
            ex_fr = row.get("explanation_fr", "").strip()
            if not ki:
                continue

            if ex_en:
                examples.append({"instruction": pick(EXPLAIN_EN), "input": ki, "output": ex_en})
            if ex_fr:
                examples.append({"instruction": pick(EXPLAIN_FR), "input": ki, "output": ex_fr})

    return examples


def export_corrections(situation_dir: Path) -> list[dict]:
    examples = []
    filepath = situation_dir / "corrections.csv"
    if not filepath.exists():
        return examples

    with open(filepath, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("review_status") != "approved":
                continue
            learner = row.get("learner_input", "").strip()
            corrected = row.get("corrected_kirundi", "").strip()
            ex_en = row.get("explanation_en", "").strip()
            if not learner or not corrected:
                continue

            output = corrected
            if ex_en:
                output = f"{corrected}\n\nExplanation: {ex_en}"

            examples.append({"instruction": pick(CORRECT), "input": learner, "output": output})

    return examples


def export_dialogues(situation_dir: Path) -> list[dict]:
    examples = []
    filepath = situation_dir / "dialogues.csv"
    if not filepath.exists():
        return examples

    # Group by dialogue_id
    dialogues: dict[str, list[dict]] = {}
    with open(filepath, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("review_status") != "approved":
                continue
            did = row.get("dialogue_id", "")
            if did:
                dialogues.setdefault(did, []).append(row)

    for did, turns in dialogues.items():
        turns.sort(key=lambda r: int(r.get("turn_number", 0)))
        situation = turns[0].get("situation", "")

        # Generate continuation examples for each turn after the first
        for i in range(1, len(turns)):
            context_lines = []
            for t in turns[:i]:
                role = t.get("speaker_role", f"Speaker {t.get('turn_number', '?')}")
                context_lines.append(f"{role}: {t['kirundi'].strip()}")
            context = "\n".join(context_lines)

            next_role = turns[i].get("speaker_role", f"Speaker {turns[i].get('turn_number', '?')}")
            next_line = turns[i]["kirundi"].strip()

            instruction = pick(DIALOGUE_CONTINUE)
            if situation:
                instruction += f" Setting: {situation}."

            examples.append({
                "instruction": instruction,
                "input": context,
                "output": f"{next_role}: {next_line}"
            })

    return examples


def export_variants(situation_dir: Path) -> list[dict]:
    examples = []
    filepath = situation_dir / "variants.csv"
    if not filepath.exists():
        return examples

    # Group by id (variant set)
    variant_sets: dict[str, list[dict]] = {}
    with open(filepath, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("review_status") != "approved":
                continue
            vid = row.get("id", "")
            if vid:
                variant_sets.setdefault(vid, []).append(row)

    for vid, variants in variant_sets.items():
        variants.sort(key=lambda r: int(r.get("variant_number", 0)))
        intent = variants[0].get("intent", "")
        situation = variants[0].get("situation", "")
        register = variants[0].get("register", "")
        n = len(variants)

        input_text = f"Situation: {situation}"
        if intent:
            input_text += f", intent: {intent}"
        if register:
            input_text += f", register: {register}"

        output_lines = []
        for v in variants:
            ki = v["kirundi"].strip()
            en = v.get("translation_en", "").strip()
            line = f"{v.get('variant_number', '?')}. {ki}"
            if en:
                line += f" ({en})"
            output_lines.append(line)

        examples.append({
            "instruction": pick(GENERATE_VARIANTS, n=n),
            "input": input_text,
            "output": "\n".join(output_lines)
        })

    return examples


def main():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    all_examples = []
    by_type = {
        "translation": [],
        "explanation": [],
        "correction": [],
        "dialogue": [],
        "variants": [],
    }

    situations = [d for d in DATA_DIR.iterdir() if d.is_dir()]

    for situation_dir in sorted(situations):
        trans = export_translations(situation_dir)
        by_type["translation"].extend(trans)
        all_examples.extend(trans)

        expl = export_explanations(situation_dir)
        by_type["explanation"].extend(expl)
        all_examples.extend(expl)

        corr = export_corrections(situation_dir)
        by_type["correction"].extend(corr)
        all_examples.extend(corr)

        dial = export_dialogues(situation_dir)
        by_type["dialogue"].extend(dial)
        all_examples.extend(dial)

        vari = export_variants(situation_dir)
        by_type["variants"].extend(vari)
        all_examples.extend(vari)

    # Write files
    def write_jsonl(filepath: Path, data: list[dict]):
        with open(filepath, "w", encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    write_jsonl(EXPORT_DIR / "training_all.jsonl", all_examples)
    for type_name, examples in by_type.items():
        write_jsonl(EXPORT_DIR / f"training_{type_name}.jsonl", examples)

    # Print summary
    print(f"Exported {len(all_examples)} total training examples:")
    for type_name, examples in by_type.items():
        print(f"  {type_name}: {len(examples)}")
    print(f"\nFiles written to {EXPORT_DIR}/")


if __name__ == "__main__":
    main()
