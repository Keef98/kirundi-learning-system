"""Unit tests for scripts.validate_csv identity and situation rules."""

import csv
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.validate_csv import EXPECTED_COLUMNS, validate_file  # noqa: E402


class TestValidateCsv(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _write_and_validate(
        self,
        file_type: str,
        rows: list[dict[str, str]],
        situation_folder: str = "greetings",
    ) -> list[str]:
        path = self.temp_dir / f"{file_type}.csv"
        columns = EXPECTED_COLUMNS[file_type]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            for row in rows:
                writer.writerow({col: row.get(col, "") for col in columns})
        return validate_file(path, file_type, situation_folder)

    @staticmethod
    def _row(row_id: str, situation: str = "greetings", **extra: str) -> dict[str, str]:
        data = {
            "id": row_id,
            "situation": situation,
            "review_status": "draft",
        }
        data.update(extra)
        return data

    @staticmethod
    def _dialogue(
        dialogue_id: str,
        turn_number: str,
        situation: str = "greetings",
    ) -> dict[str, str]:
        return {
            "dialogue_id": dialogue_id,
            "situation": situation,
            "turn_number": turn_number,
            "review_status": "draft",
        }

    @staticmethod
    def _variant(
        row_id: str,
        variant_number: str,
        situation: str = "greetings",
    ) -> dict[str, str]:
        return {
            "id": row_id,
            "situation": situation,
            "intent": "greet",
            "variant_number": variant_number,
            "source_type": "original",
            "review_status": "draft",
        }

    def test_duplicate_translation_id(self) -> None:
        errors = self._write_and_validate(
            "translations",
            [
                self._row("greet_tr_001", source_type="original"),
                self._row("greet_tr_001", source_type="original"),
            ],
        )
        self.assertTrue(any("duplicate id" in e for e in errors), errors)

    def test_duplicate_explanation_id(self) -> None:
        errors = self._write_and_validate(
            "explanations",
            [
                self._row("greet_ex_001", source_type="original"),
                self._row("greet_ex_001", source_type="original"),
            ],
        )
        self.assertTrue(any("duplicate id" in e for e in errors), errors)

    def test_duplicate_correction_id(self) -> None:
        errors = self._write_and_validate(
            "corrections",
            [
                self._row("greet_co_001"),
                self._row("greet_co_001"),
            ],
        )
        self.assertTrue(any("duplicate id" in e for e in errors), errors)

    def test_same_dialogue_id_same_turn(self) -> None:
        errors = self._write_and_validate(
            "dialogues",
            [
                self._dialogue("greet_dl_001", "1"),
                self._dialogue("greet_dl_001", "1"),
            ],
        )
        self.assertTrue(any("duplicate dialogue_id" in e for e in errors), errors)

    def test_same_dialogue_id_different_turn(self) -> None:
        errors = self._write_and_validate(
            "dialogues",
            [
                self._dialogue("greet_dl_001", "1"),
                self._dialogue("greet_dl_001", "2"),
            ],
        )
        self.assertEqual(errors, [])

    def test_same_variant_id_same_number(self) -> None:
        errors = self._write_and_validate(
            "variants",
            [
                self._variant("greet_va_001", "1"),
                self._variant("greet_va_001", "1"),
            ],
        )
        self.assertTrue(any("duplicate id" in e for e in errors), errors)
        self.assertTrue(any("variant_number" in e for e in errors), errors)

    def test_same_variant_id_different_number(self) -> None:
        errors = self._write_and_validate(
            "variants",
            [
                self._variant("greet_va_001", "1"),
                self._variant("greet_va_001", "2"),
            ],
        )
        self.assertEqual(errors, [])

    def test_correct_situation(self) -> None:
        errors = self._write_and_validate(
            "translations",
            [self._row("greet_tr_001", situation="greetings", source_type="original")],
            situation_folder="greetings",
        )
        self.assertEqual(errors, [])

    def test_wrong_situation(self) -> None:
        errors = self._write_and_validate(
            "translations",
            [self._row("greet_tr_001", situation="market", source_type="original")],
            situation_folder="greetings",
        )
        self.assertTrue(any("does not match folder" in e for e in errors), errors)

    def test_blank_situation(self) -> None:
        errors = self._write_and_validate(
            "translations",
            [self._row("greet_tr_001", situation="", source_type="original")],
            situation_folder="greetings",
        )
        self.assertTrue(any("does not match folder" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
