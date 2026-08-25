#!/usr/bin/env python3
"""The live Domain Architect path must not revive SFE or HB."""

from __future__ import annotations

import ast
import hashlib
import unittest
from pathlib import Path

from domain_architect.app import handle_api
from domain_architect.audit import audit_expression
from domain_architect.compatibility import Transformation
from domain_architect.decompose import decompose
from domain_architect.realization import realize_second_order
from domain_architect.translate import mechanical_electrical_translation


LIVE_FORBIDDEN = (
    "canonical sfe",
    "simons field equation",
    "unified harmonic framework",
    "harmonic blueprint",
    "uhf",
    "dhfa",
    "d_master",
    "c_master",
    "q_uhf",
    "k_dhfa",
)

LIVE_ROOT = Path(__file__).resolve().parents[1] / "domain_architect"
ARCHIVE_QSTACK = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "archive"
    / "qstack"
    / "qstack_regularity_paper.pdf"
)
QSTACK_SHA256 = (
    "3ea9a93ac39d35e773f550c12b6f1e643f6fd65247ccf9b094d108789e7f96e8"
)
ARCHIVE_PRIME_FIELD = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "archive"
    / "prime-field-2026-08-25"
)
PRIME_FIELD_COHERENCE_SHA256 = (
    "62728c7436fa7bd3093ed8a18da155eee22fd6bbe4121378aaf5df4273a9decf"
)
MAY16_TRACK_B_SHA256 = (
    "477a857f8ab4e066d1ef2be7e05786a4dd101cd31b325ab484e4f0ddef11f6cd"
)
ARCHIVE_SFE_HB = (
    Path(__file__).resolve().parents[1] / "docs" / "archive" / "sfe-hb"
)
UHSA_SYNTHESIS = (
    ARCHIVE_SFE_HB
    / "Unified_Harmonic_Spectral_Architecture_Session_Master_Synthesis_2026-08-19.md"
)
UHSA_SYNTHESIS_SHA256 = (
    "2baa96ea58fb8a42c385c26495a5a034cd6a406ff7f865c7c294506adfe31b1e"
)
LIVE_FORBIDDEN_TOKENS = (
    "d_master",
    "c_master",
    "q_uhf",
    "k_dhfa",
)


class TestLivePathDropsSfeHb(unittest.TestCase):
    def test_oscillator_report_is_domain_architect(self):
        report = audit_expression("m*xdd + c*xd + k*x = f")
        narrative = report.narrative().lower()
        self.assertIn("decompose", narrative)
        for phrase in LIVE_FORBIDDEN:
            self.assertNotIn(phrase, narrative)

    def test_schema_does_not_export_sfe_status(self):
        import domain_architect.schema as schema

        self.assertFalse(hasattr(schema, "CANONICAL_SFE_STATUS"))
        self.assertTrue(hasattr(schema, "PRIMARY_OPERATIONS"))

    def test_core_modules_do_not_import_historical(self):
        root = Path(__file__).resolve().parents[1] / "domain_architect"
        banned = {"historical", "prime_field_coherence"}
        live = [
            "decompose.py",
            "translate.py",
            "synthesize.py",
            "compatibility.py",
            "cycle.py",
            "realization.py",
            "audit.py",
            "classify.py",
            "leftover_repair.py",
            "lab_cases.py",
            "localized_repair.py",
        ]
        for name in live:
            source = (root / name).read_text(encoding="utf-8")
            self.assertNotIn(
                "prime_field_coherence",
                source,
                f"{name} must not mention the archived Prime Field sketch",
            )
            tree = ast.parse(source)
            imported = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    imported.add(node.module.split(".")[-1])
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported.add(alias.name.split(".")[-1])
            self.assertFalse(
                imported & banned,
                f"{name} imports historical archive modules: {imported & banned}",
            )
            hay = source.lower()
            for token in LIVE_FORBIDDEN_TOKENS:
                self.assertNotIn(
                    token,
                    hay,
                    f"{name} must not contain archived UHSA token {token!r}",
                )


class TestExecutableTransformation(unittest.TestCase):
    def test_apply_remaps_coefficients(self):
        t = Transformation(name="firestone", mapping={"m": "L", "c": "R", "k": "1/C"})
        out = t.apply({"m": 2.0, "c": 0.4, "k": 3.0})
        self.assertEqual(out["L"], 2.0)
        self.assertEqual(out["R"], 0.4)
        self.assertTrue(t.applied)
        self.assertFalse(t.is_identity())

    def test_mechanical_electrical_is_transformable_not_equivalent(self):
        record = mechanical_electrical_translation()
        self.assertEqual(record.kind.value, "mathematical_correspondence")
        self.assertTrue(all(c.transformation and c.transformation.applied for c in record.compatibility))
        kinds = {c.kind.value for c in record.compatibility}
        self.assertNotIn("structure_preserving_equivalence", kinds)


class TestRealization(unittest.TestCase):
    def test_free_response_decays(self):
        real = realize_second_order(omega=2.0, zeta=0.25, t_final=6.0)
        self.assertLess(abs(real.y[-1]), abs(real.y[0]))
        self.assertIn("standard", real.method.lower())


class TestDesktopApi(unittest.TestCase):
    def test_status_and_decompose(self):
        status, body, _ctype = handle_api("/api/status", {})
        self.assertEqual(status, 200)
        payload = __import__("json").loads(body)
        self.assertIn("DECOMPOSE", payload["operations"])
        self.assertIn("archived", payload["historical_note"].lower())

        status, body, _ctype = handle_api("/api/decompose", {"expression": "m*xdd + c*xd + k*x = f"})
        self.assertEqual(status, 200)
        report = __import__("json").loads(body)
        text = report["narrative"].lower()
        self.assertIn("domain architect", text)
        self.assertNotIn("canonical sfe", text)

    def test_archive_is_opt_in(self):
        status, body, _ctype = handle_api("/api/archive", {})
        self.assertEqual(status, 200)
        payload = __import__("json").loads(body)
        ids = [eq["equation_id"] for eq in payload["equations"]]
        self.assertIn("SFE-H001", ids)


class TestQstackRegularityPdfStaysArchived(unittest.TestCase):
    def test_pdf_is_in_archive_not_in_live_package(self):
        self.assertTrue(ARCHIVE_QSTACK.is_file(), ARCHIVE_QSTACK)
        raw = ARCHIVE_QSTACK.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), QSTACK_SHA256)
        self.assertEqual(len(raw), 191238)
        self.assertFalse((LIVE_ROOT / "qstack.py").is_file())
        self.assertFalse((LIVE_ROOT / "qnav.py").is_file())
        note = ARCHIVE_QSTACK.parent.joinpath("README.md").read_text(encoding="utf-8")
        self.assertIn("archive only", note.lower())
        self.assertIn("Not Clay", note)
        self.assertIn("Not live Domain Architect", note)
        self.assertIn("import into `domain_architect/`", note)
        archive_index = (
            Path(__file__).resolve().parents[1] / "docs" / "archive" / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("qstack/", archive_index)
        self.assertIn("not live DA", archive_index)
        self.assertNotIn("qstack_regularity", " ".join(p.name for p in LIVE_ROOT.iterdir()))


class TestPrimeFieldBatchStaysArchived(unittest.TestCase):
    def test_coherence_py_is_in_archive_not_in_live_package(self):
        py = ARCHIVE_PRIME_FIELD / "prime_field_coherence.py"
        self.assertTrue(py.is_file(), py)
        raw = py.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), PRIME_FIELD_COHERENCE_SHA256)
        self.assertEqual(len(raw), 23513)
        self.assertFalse((LIVE_ROOT / "prime_field_coherence.py").is_file())
        self.assertFalse((LIVE_ROOT / "sfe.py").is_file())
        self.assertFalse((LIVE_ROOT / "uhf.py").is_file())
        self.assertFalse((LIVE_ROOT / "dhfa.py").is_file())
        note = ARCHIVE_PRIME_FIELD.joinpath("README.md").read_text(encoding="utf-8")
        self.assertIn("archive only", note.lower())
        self.assertIn("Not live Domain Architect", note)
        self.assertIn("NOT CLAIMED", note)
        self.assertIn("import into `domain_architect/`", note)
        self.assertIn("not live da", note.lower())
        self.assertIn("Do not stamp DA-VC-01", note)
        self.assertNotIn("DA-VC-01 PASS", note)
        archive_index = (
            Path(__file__).resolve().parents[1] / "docs" / "archive" / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("prime-field-2026-08-25/", archive_index)
        self.assertIn("not live DA", archive_index)
        self.assertNotIn(
            "prime_field_coherence",
            " ".join(p.name for p in LIVE_ROOT.iterdir()),
        )

    def test_may16_track_b_was_duplicate_swirl_face_not_sfe(self):
        may = (
            Path(__file__).resolve().parents[1]
            / "docs"
            / "papers"
            / "swirl"
            / "zenodo-may"
            / "PhiRenorm_TrackB.pdf"
        )
        self.assertTrue(may.is_file(), may)
        self.assertEqual(hashlib.sha256(may.read_bytes()).hexdigest(), MAY16_TRACK_B_SHA256)
        self.assertEqual(may.stat().st_size, 13524)
        self.assertFalse((ARCHIVE_PRIME_FIELD / "PhiRenorm_TrackB_May16.pdf").is_file())
        self.assertFalse((ARCHIVE_PRIME_FIELD / "PhiRenorm_TrackB.pdf").is_file())
        faces = (
            Path(__file__).resolve().parents[1]
            / "docs"
            / "papers"
            / "swirl"
            / "FACES.md"
        ).read_text(encoding="utf-8")
        self.assertIn("PhiRenorm_TrackB_May16_e075.pdf", faces)
        self.assertIn("duplicate", faces.lower())
        self.assertIn("**Not** SFE", faces)


class TestUhsaSessionSynthesisStaysArchived(unittest.TestCase):
    """19 Aug 2026 UHSA dump stays historical. Live DA must not import it."""

    def test_synthesis_is_in_archive_not_in_live_package(self):
        self.assertTrue(UHSA_SYNTHESIS.is_file(), UHSA_SYNTHESIS)
        raw = UHSA_SYNTHESIS.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), UHSA_SYNTHESIS_SHA256)
        self.assertEqual(len(raw), 15924)
        text = raw.decode("utf-8")
        self.assertIn("Historical session synthesis only", text)
        self.assertIn("Not live Domain Architect", text)
        self.assertIn("NOT CLAIMED", text)
        self.assertIn("Not June Paper2 FIXED", text)
        self.assertIn("Not QStack product", text)
        self.assertIn("import into `domain_architect/`", text)
        self.assertIn("HN = D^((-1)/2)*Qtilde*D^((-1)/2)", text)
        self.assertIn("Action 1 is inverted", text)
        self.assertIn("§8 hurdles stay OPEN", text)
        self.assertIn("D_Master", text)
        self.assertIn("C_Master", text)
        self.assertIn("Q_UHF", text)
        self.assertIn("K_DHFA", text)
        self.assertFalse((LIVE_ROOT / "sfe.py").is_file())
        self.assertFalse((LIVE_ROOT / "uhf.py").is_file())
        self.assertFalse((LIVE_ROOT / "dhfa.py").is_file())
        self.assertFalse((LIVE_ROOT / "d_master.py").is_file())
        self.assertFalse((LIVE_ROOT / "c_master.py").is_file())
        self.assertFalse((LIVE_ROOT / "q_uhf.py").is_file())
        self.assertFalse((LIVE_ROOT / "k_dhfa.py").is_file())
        live_names = " ".join(p.name for p in LIVE_ROOT.iterdir())
        self.assertNotIn("d_master", live_names)
        self.assertNotIn("c_master", live_names)
        note = ARCHIVE_SFE_HB.joinpath("README.md").read_text(encoding="utf-8")
        self.assertIn("archive only", note.lower())
        self.assertIn("Not live Domain Architect", note)
        self.assertIn("NOT CLAIMED", note)
        self.assertIn("import into `domain_architect/`", note)
        self.assertIn("Action 1 is inverted", note)
        self.assertIn("Do not stamp DA-VC-01", note)
        self.assertIn("DA-VC-01 remains **FAIL**", note)
        self.assertNotIn("DA-VC-01 PASS", note)
        archive_index = (
            Path(__file__).resolve().parents[1] / "docs" / "archive" / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("sfe-hb/", archive_index)
        self.assertIn("not live DA", archive_index)
        lookup = (
            Path(__file__).resolve().parents[1]
            / "docs"
            / "packets"
            / "OLD-PAPERS-LOOK-UP.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "Unified_Harmonic_Spectral_Architecture_Session_Master_Synthesis_2026-08-19.md",
            lookup,
        )
        faces = (
            Path(__file__).resolve().parents[1]
            / "docs"
            / "papers"
            / "ns-snd"
            / "FACES.md"
        ).read_text(encoding="utf-8")
        self.assertIn("sfe-hb/", faces)
        self.assertIn("Not** a Paper2 face", faces)
        gcd = (
            Path(__file__).resolve().parents[1] / "docs" / "papers" / "gcd" / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("sfe-hb/", gcd)
        self.assertIn("Do not glue it to NS regularity", gcd)

    def test_live_package_has_no_uhsa_master_operators(self):
        skip = {"historical.py"}
        for path in sorted(LIVE_ROOT.glob("*.py")):
            if path.name in skip:
                continue
            hay = path.read_text(encoding="utf-8").lower()
            for token in LIVE_FORBIDDEN_TOKENS:
                self.assertNotIn(
                    token,
                    hay,
                    f"{path.name} must not contain archived UHSA token {token!r}",
                )


class TestNoPaddedParameterLevel(unittest.TestCase):
    def test_mechanism_is_not_wrapped_in_dummy_parameter(self):
        dec = decompose("m*xdd + c*xd + k*x = f")
        levels = {n.level for n in dec.tree.walk()}
        self.assertIn("MECHANISM", levels)
        self.assertNotIn("PARAMETER", levels)


if __name__ == "__main__":
    unittest.main()
