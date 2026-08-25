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
    "4d49cd1ee629e6c2fbf0ad93fa08c107d6d4587ea5a06121930ecbdeb848e363"
)
SPECTRAL_UNIFICATION_TEX = ARCHIVE_SFE_HB / "SPECTRAL_UNIFICATION_PAPER.tex"
SPECTRAL_UNIFICATION_NOTE = ARCHIVE_SFE_HB / "SPECTRAL_UNIFICATION_PAPER.md"
SPECTRAL_UNIFICATION_SHA256 = (
    "4ea7ccd72dc60d773e603aee0328a10ad254376c465d1ee1ddee849d35f2291c"
)
EQUATION_EXPLORER = ARCHIVE_SFE_HB / "equation_explorer_simons_field.py"
EQUATION_EXPLORER_SHA256 = (
    "191d0738ed9f6703793388dc9545dd6c9f9f67b2eb9647cb535b445f0f921743"
)
LIVE_FORBIDDEN_TOKENS = (
    "d_master",
    "c_master",
    "q_uhf",
    "k_dhfa",
    "simons_field",
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
        banned = {"historical", "prime_field_coherence", "simons_field"}
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
            "open_board.py",
            "turbulence_intensity.py",
            "available_turbulence.py",
        ]
        for name in live:
            source = (root / name).read_text(encoding="utf-8")
            self.assertNotIn(
                "prime_field_coherence",
                source,
                f"{name} must not mention the archived Prime Field sketch",
            )
            self.assertNotIn(
                "simons_field",
                source,
                f"{name} must not mention the archived Equation Explorer",
            )
            self.assertNotIn(
                "equation explorer",
                source.lower(),
                f"{name} must not host the archived Equation Explorer",
            )
            self.assertNotIn(
                "sfe_field",
                source,
                f"{name} must not mention the archived SFE black-hole toy",
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
        self.assertNotIn("equation explorer", text)

    def test_desktop_html_has_no_equation_explorer_tab(self):
        html = (LIVE_ROOT / "static" / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("Equation Explorer", html)
        self.assertNotIn("simons_field", html)
        self.assertNotIn("Black Hole Simulator", html)
        self.assertNotIn("sfe_field", html)
        self.assertIn("DECOMPOSE", html)

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
        self.assertEqual(len(raw), 15899)
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


class TestSpectralUnificationPaperArchived(unittest.TestCase):
    """Frankie SPECTRAL_UNIFICATION_PAPER.tex is archive-only overclaim. Not Clay."""

    def test_tex_is_archived_not_live_and_not_proved(self):
        self.assertTrue(SPECTRAL_UNIFICATION_TEX.is_file(), SPECTRAL_UNIFICATION_TEX)
        self.assertTrue(SPECTRAL_UNIFICATION_NOTE.is_file(), SPECTRAL_UNIFICATION_NOTE)
        self.assertFalse(
            (ARCHIVE_SFE_HB / "SPECTRAL_UNIFICATION_PAPER.MISSING.md").is_file()
        )
        self.assertFalse((LIVE_ROOT / "SPECTRAL_UNIFICATION_PAPER.tex").is_file())
        raw = SPECTRAL_UNIFICATION_TEX.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), SPECTRAL_UNIFICATION_SHA256)
        self.assertEqual(len(raw), 10586)
        tex = raw.decode("utf-8")
        self.assertIn(r"\title{\textbf{One Operator, Three Millennia}", tex)
        self.assertIn("June 10, 2026", tex)
        self.assertIn("UNIF-JS-2026", tex)
        self.assertIn("Status: Proved", tex)
        note = SPECTRAL_UNIFICATION_NOTE.read_text(encoding="utf-8")
        self.assertIn("4ea7ccd72dc6", note)
        self.assertIn("7d5c64a34_SPECTRAL_UNIFICATION_PAPER", note)
        self.assertIn("HTTP **302**", note)
        self.assertIn("**200**", note)
        self.assertIn("**403**", note)
        self.assertIn("NOT CLAIMED", note)
        self.assertIn("rejected", note.lower())
        self.assertIn("withdrawn", note.lower())
        self.assertIn("Not live Domain Architect", note)
        self.assertIn("7de9444d", note)
        self.assertIn("f51ed5c05ec3", note)
        self.assertIn("SND_GNC_BRIDGE_EXTRACTED.txt", note)
        self.assertIn("import into `domain_architect/`", note)
        readme = ARCHIVE_SFE_HB.joinpath("README.md").read_text(encoding="utf-8")
        self.assertIn("SPECTRAL_UNIFICATION_PAPER.tex", readme)
        self.assertIn("7d5c64a34_", readme)
        self.assertIn("import into `domain_architect/`", readme)
        archive_index = (
            Path(__file__).resolve().parents[1] / "docs" / "archive" / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("SPECTRAL_UNIFICATION_PAPER.md", archive_index)
        self.assertIn("4ea7ccd72dc6", archive_index)
        lookup = (
            Path(__file__).resolve().parents[1]
            / "docs"
            / "packets"
            / "OLD-PAPERS-LOOK-UP.md"
        ).read_text(encoding="utf-8")
        self.assertIn("7d5c64a34_SPECTRAL_UNIFICATION_PAPER.tex", lookup)
        self.assertIn("archived", lookup.lower())
        faces = (
            Path(__file__).resolve().parents[1]
            / "docs"
            / "papers"
            / "ns-snd"
            / "FACES.md"
        ).read_text(encoding="utf-8")
        self.assertIn("SPECTRAL_UNIFICATION_PAPER.tex", faces)
        self.assertIn("**Not** a Paper2 face", faces)
        self.assertIn("**Not** a compile of the FIXED PDF", faces)
        self.assertIn("4ea7ccd72dc6", faces)
        for path in LIVE_ROOT.glob("*.py"):
            self.assertNotIn(
                "SPECTRAL_UNIFICATION",
                path.read_text(encoding="utf-8"),
                path.name,
            )


class TestEquationExplorerStaysArchived(unittest.TestCase):
    """Jon matplotlib SFE slider paste stays historical. Live DA must not import it."""

    def test_script_is_in_archive_not_in_live_package(self):
        self.assertTrue(EQUATION_EXPLORER.is_file(), EQUATION_EXPLORER)
        raw = EQUATION_EXPLORER.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), EQUATION_EXPLORER_SHA256)
        self.assertEqual(len(raw), 3730)
        text = raw.decode("utf-8")
        self.assertIn("Historical toy only", text)
        self.assertIn("Not live Domain Architect", text)
        self.assertIn("NOT CLAIMED", text)
        self.assertIn("Not June Paper2 FIXED", text)
        self.assertIn("Not Ring SND", text)
        self.assertIn("Not Q6 H_N", text)
        self.assertIn("does not depend on x", text)
        self.assertIn("phi += A * sin(2*pi*f*t/spatial_mod + delta)", text)
        self.assertIn(
            "phi += A * np.sin(2 * np.pi * f * t / spatial_mod + delta)",
            text,
        )
        self.assertIn("Equation Explorer: Simons Field", text)
        self.assertIn("import into `domain_architect/`", text)
        self.assertIn("Do not add an Equation Explorer tab", text)
        self.assertIn("prime_field_coherence.py", text)
        self.assertIn("def simons_field", text)
        self.assertIn("init_spatial_mod = 1.618", text)
        self.assertIn("init_primes = [2, 3, 5, 7, 11]", text)
        self.assertIn("plt.show()", text)
        self.assertFalse((LIVE_ROOT / "equation_explorer_simons_field.py").is_file())
        self.assertFalse((LIVE_ROOT / "simons_field.py").is_file())
        self.assertFalse((LIVE_ROOT / "sfe.py").is_file())
        live_names = " ".join(p.name for p in LIVE_ROOT.iterdir())
        self.assertNotIn("equation_explorer", live_names)
        self.assertNotIn("simons_field", live_names)
        note = ARCHIVE_SFE_HB.joinpath("README.md").read_text(encoding="utf-8")
        self.assertIn("archive only", note.lower())
        self.assertIn("Not live Domain Architect", note)
        self.assertIn("NOT CLAIMED", note)
        self.assertIn("import into `domain_architect/`", note)
        self.assertIn("does not depend on `x`", note)
        self.assertIn("Do not add an Equation Explorer tab", note)
        self.assertIn("equation_explorer_simons_field.py", note)
        self.assertIn("sfe_black_hole_simulator_paste.py", note)
        self.assertIn("chat paste arrived", note.lower())
        self.assertIn("Do not stamp DA-VC-01", note)
        self.assertNotIn("DA-VC-01 PASS", note)
        archive_index = (
            Path(__file__).resolve().parents[1] / "docs" / "archive" / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("sfe-hb/", archive_index)
        self.assertIn("equation_explorer_simons_field.py", archive_index)
        self.assertIn("not live DA", archive_index)
        self.assertIn("Do not add an Equation Explorer tab", archive_index)
        lookup = (
            Path(__file__).resolve().parents[1]
            / "docs"
            / "packets"
            / "OLD-PAPERS-LOOK-UP.md"
        ).read_text(encoding="utf-8")
        self.assertIn("equation_explorer_simons_field.py", lookup)
        self.assertIn("does not depend on `x`", lookup)
        self.assertIn("sfe_black_hole_simulator_paste.py", lookup)
        self.assertIn("SFE Black Hole Simulator", lookup)
        faces = (
            Path(__file__).resolve().parents[1]
            / "docs"
            / "papers"
            / "ns-snd"
            / "FACES.md"
        ).read_text(encoding="utf-8")
        self.assertIn("equation_explorer_simons_field.py", faces)
        self.assertIn("Not** a Paper2 face", faces)
        self.assertIn("sfe_black_hole_simulator_paste.py", faces)
        swirl = (
            Path(__file__).resolve().parents[1]
            / "docs"
            / "papers"
            / "swirl"
            / "FACES.md"
        ).read_text(encoding="utf-8")
        self.assertIn("equation_explorer_simons_field.py", swirl)
        self.assertIn(r"\Phi=u_\theta/r", swirl)
        self.assertIn("sfe_black_hole_simulator_paste.py", swirl)
        gcd = (
            Path(__file__).resolve().parents[1] / "docs" / "papers" / "gcd" / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("sfe-hb/", gcd)
        self.assertIn("not** q6", gcd.lower())
        ring = (
            Path(__file__).resolve().parents[1]
            / "docs"
            / "papers"
            / "ring"
            / "FACES.md"
        ).read_text(encoding="utf-8")
        self.assertIn("equation_explorer_simons_field.py", ring)
        self.assertIn("Not** Ring SND", ring)
        self.assertIn("sfe_black_hole_simulator_paste.py", ring)
        html = (LIVE_ROOT / "static" / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("Equation Explorer", html)
        self.assertNotIn("simons_field", html)
        self.assertNotIn("Black Hole Simulator", html)
        self.assertNotIn("sfe_field", html)
        for path in sorted(LIVE_ROOT.glob("*.py")):
            if path.name == "historical.py":
                continue
            hay = path.read_text(encoding="utf-8")
            self.assertNotIn("simons_field", hay, path.name)
            self.assertNotIn("Equation Explorer", hay, path.name)
            self.assertNotIn("sfe_field", hay, path.name)
            self.assertNotIn("Black Hole Simulator", hay, path.name)

    def test_live_package_has_no_equation_explorer_module(self):
        self.assertFalse((LIVE_ROOT / "equation_explorer_simons_field.py").is_file())
        static_hits = list((LIVE_ROOT / "static").rglob("*explorer*"))
        self.assertEqual(static_hits, [])


class TestAprilOverleafExportsStayQuarantined(unittest.TestCase):
    """CLAY_FINAL / SERPENT / simons_ns_overleaf / WHAT_I_FOUND are not DA."""

    ROOT = Path(__file__).resolve().parents[1]
    LIVE_ROOT = ROOT / "domain_architect"
    QUARANTINE = ROOT / "docs" / "archive" / "overleaf-2026-04"
    POLICY = ROOT / "docs" / "packets" / "OVERLEAF-VS-PACK-AUDIT-2026-08-15.md"
    PRODUCT_MODULES = (
        "clay_final.py",
        "serpent.py",
        "serpent_final.py",
        "what_i_found.py",
        "simons_ns_overleaf.py",
        "overleaf_package.py",
        "CLAY_FINAL.py",
        "SERPENT_FINAL.py",
    )
    EXPORT_TREES = (
        "219709d19_CLAY_FINAL_OVERLEAF",
        "e399df8e7_SERPENT_FINAL_OVERLEAF",
        "8a2077729_WHAT_I_FOUND_OVERLEAF",
        "b6e5416c8_simons_ns_overleaf",
        "3673bad0d_simons_overleaf_FINAL",
        "overleaf_package",
    )
    LIVE_MODULES = (
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
    )

    def test_live_package_has_no_overleaf_product_modules(self):
        for name in self.PRODUCT_MODULES:
            self.assertFalse(
                (self.LIVE_ROOT / name).is_file(),
                f"do not import Overleaf museum {name} into live DA",
            )
        live_names = " ".join(p.name for p in self.LIVE_ROOT.iterdir())
        for token in (
            "clay_final",
            "serpent_final",
            "what_i_found",
            "simons_ns_overleaf",
            "overleaf_package",
        ):
            self.assertNotIn(token, live_names)
        for tree in self.EXPORT_TREES:
            self.assertFalse((self.LIVE_ROOT / tree).exists(), tree)
            self.assertFalse((self.QUARANTINE / tree).exists(), tree)
        for folder in (self.ROOT / "docs", self.LIVE_ROOT):
            for name in ("CLAY_FINAL.tex", "SERPENT_FINAL.tex", "WHAT_I_FOUND.tex"):
                hits = list(folder.rglob(name))
                self.assertEqual(hits, [], hits)

    def test_core_modules_do_not_import_overleaf_museum(self):
        banned = {
            "clay_final",
            "serpent_final",
            "what_i_found",
            "simons_ns_overleaf",
            "overleaf_package",
            "CLAY_FINAL",
            "SERPENT_FINAL",
            "WHAT_I_FOUND",
        }
        for name in self.LIVE_MODULES:
            source = (self.LIVE_ROOT / name).read_text(encoding="utf-8")
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
                f"{name} imports Overleaf museum: {imported & banned}",
            )
            hay = source
            for token in (
                "CLAY_FINAL",
                "SERPENT_FINAL",
                "WHAT_I_FOUND",
                "simons_ns_overleaf",
            ):
                self.assertNotIn(
                    token,
                    hay,
                    f"{name} must not load Overleaf museum token {token!r}",
                )

    def test_quarantine_receipt_and_policy_are_filed(self):
        receipt = self.QUARANTINE / "OVERLEAF-EXPORTS.MISSING.md"
        note = self.QUARANTINE / "README.md"
        self.assertTrue(self.POLICY.is_file(), self.POLICY)
        self.assertTrue(receipt.is_file(), receipt)
        self.assertTrue(note.is_file(), note)
        policy = self.POLICY.read_text(encoding="utf-8")
        missing = receipt.read_text(encoding="utf-8")
        banner = note.read_text(encoding="utf-8")
        self.assertIn("Policy banner", policy)
        self.assertIn("not a new", policy.lower())
        self.assertIn("Ignore existing Overleaf projects", policy)
        self.assertIn("PDF printer", policy)
        self.assertIn("No Overleaf login", policy)
        self.assertIn("NOT CLAIMED", policy)
        self.assertIn("DA-VC-01", policy)
        self.assertIn("FAIL", policy)
        self.assertIn("not received", missing.lower())
        self.assertIn("Do **not** invent TeX", missing)
        self.assertIn("quarantine", banner.lower())
        self.assertIn("import into `domain_architect/`", banner)
        for token in (
            "CLAY_FINAL",
            "SERPENT_FINAL",
            "WHAT_I_FOUND",
            "simons_ns_overleaf",
            "overleaf_package",
        ):
            self.assertIn(token, missing)
            self.assertIn(token, policy)
        self.assertNotIn("\\title{", missing)
        self.assertNotIn("\\begin{document}", missing)
        self.assertNotIn("DA-VC-01 PASS", policy)
        archive_index = (self.ROOT / "docs" / "archive" / "README.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("overleaf-2026-04/", archive_index)
        self.assertIn("OVERLEAF-VS-PACK-AUDIT-2026-08-15.md", archive_index)
        lookup = (
            self.ROOT / "docs" / "packets" / "OLD-PAPERS-LOOK-UP.md"
        ).read_text(encoding="utf-8")
        self.assertIn("OVERLEAF-VS-PACK-AUDIT-2026-08-15.md", lookup)
        self.assertIn("not received", lookup.lower())
        qstack = (
            self.ROOT / "docs" / "archive" / "qstack" / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("overleaf_package", qstack)
        self.assertIn("not received", qstack.lower())


class TestNoPaddedParameterLevel(unittest.TestCase):
    def test_mechanism_is_not_wrapped_in_dummy_parameter(self):
        dec = decompose("m*xdd + c*xd + k*x = f")
        levels = {n.level for n in dec.tree.walk()}
        self.assertIn("MECHANISM", levels)
        self.assertNotIn("PARAMETER", levels)


if __name__ == "__main__":
    unittest.main()
