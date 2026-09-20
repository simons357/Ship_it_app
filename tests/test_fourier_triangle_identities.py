"""Guardrails for the Fourier-triangle reconstruction."""

from __future__ import annotations

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.fourier_triangle_identities as ft  # noqa: E402

DOC = ROOT / "docs" / "ns-review" / "FOURIER-TRIANGLE-MECHANISM.md"


class TestFourierTriangleIdentities(unittest.TestCase):
    def test_doc_tags_and_missing_arrow(self) -> None:
        self.assertTrue(DOC.is_file(), f"missing {DOC}")
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("**EXACT**", text)
        self.assertIn("**CLAIMED**", text)
        self.assertIn("**NOT SEATED**", text)
        self.assertIn("I₃ prime restrictions", text)
        self.assertIn(r"\not\Longrightarrow", text)
        self.assertIn(r"T_c", text)
        self.assertIn(r"\theta\nu D_s", text)
        self.assertNotIn("Clay Millennium solved", text)
        self.assertIn("Do not repair Theorem H", text)

    def test_equal_length(self) -> None:
        ft.assert_equal_length()

    def test_unequal_defect(self) -> None:
        ft.assert_unequal_length_defect()

    def test_leray(self) -> None:
        ft.assert_leray_kills_parallel()

    def test_im_vs_abs(self) -> None:
        ft.assert_im_is_not_abs()


if __name__ == "__main__":
    unittest.main()
