"""DA proof: write the NS chain; emit is not QED."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_attempt import is_attempt_ask  # noqa: E402
from da_brute import is_brute_ask  # noqa: E402
from da_hunt import is_look_ask  # noqa: E402
from da_picture import is_picture_ask  # noqa: E402
from da_proof import (  # noqa: E402
    A_LINES,
    CLAIMS,
    LINES,
    PROBLEMS,
    is_all_ask,
    is_proof_ask,
    parse_problem,
    parse_problems,
    run,
)


class DaProofTests(unittest.TestCase):
    def test_writes_the_chain(self):
        tmp = Path(tempfile.mkdtemp()) / "da_proof_test.json"
        payload = run(out=tmp)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["C1"]["verdict"], "pass")
        self.assertEqual(by["C2"]["verdict"], "pass")
        self.assertEqual(by["C3"]["verdict"], "fail")
        self.assertEqual(by["C4"]["verdict"], "fail")
        self.assertEqual(by["C5"]["verdict"], "fail")
        self.assertEqual(by["C6"]["verdict"], "open")
        self.assertEqual(by["C7"]["verdict"], "fail")
        self.assertEqual(by["C8"]["verdict"], "open")
        self.assertEqual(by["C9"]["verdict"], "fail")
        self.assertEqual(by["C10"]["verdict"], "fail")
        self.assertEqual(by["C11"]["verdict"], "fail")
        self.assertEqual(by["C12"]["verdict"], "fail")
        self.assertEqual(by["C13"]["verdict"], "fail")
        self.assertEqual(by["C14"]["verdict"], "fail")
        self.assertEqual(by["C15"]["verdict"], "fail")
        self.assertEqual(by["C16"]["verdict"], "pass")
        self.assertEqual(by["C17"]["verdict"], "fail")
        self.assertEqual(by["C18"]["verdict"], "fail")
        self.assertEqual(by["C19"]["verdict"], "fail")
        self.assertEqual(by["C20"]["verdict"], "fail")
        self.assertTrue(payload["meta"]["nothing_wrong_with_asking"])
        self.assertTrue(payload["meta"]["q_is_not_rh"])
        self.assertTrue(payload["meta"]["a_is_not_b"])
        self.assertEqual(payload["problem"], "NS")
        self.assertEqual(payload["counts"]["write"], 1)
        self.assertEqual([L["status"] for L in LINES], ["have"] * 5 + ["write"] + ["follows"] * 3)
        self.assertEqual([L["status"] for L in A_LINES], ["have"] * 6 + ["write"] + ["follows"] * 2)
        self.assertTrue(is_proof_ask("write me the proof chain for Navier-Stokes"))
        self.assertTrue(is_proof_ask("Xavier Stokes"))
        self.assertTrue(is_proof_ask("proof chain"))
        self.assertTrue(is_proof_ask("Track B please write"))
        self.assertEqual(parse_problem(ask="Track B please write"), "NS")
        self.assertFalse(is_look_ask("Track B please write"))
        self.assertFalse(is_brute_ask("Track B please write"))
        self.assertFalse(is_picture_ask("Track B please write"))
        self.assertFalse(is_attempt_ask("Track B please write"))
        both_ask = "Track B please write. track A write as well please."
        self.assertTrue(is_proof_ask(both_ask))
        self.assertFalse(is_attempt_ask(both_ask))
        self.assertEqual(parse_problems(ask=both_ask), ["NS", "A"])
        as_well = "Track B please write   Track a as well"
        self.assertTrue(is_proof_ask(as_well))
        self.assertFalse(is_attempt_ask(as_well))
        self.assertEqual(parse_problems(ask=as_well), ["NS", "A"])
        self.assertTrue(is_proof_ask("track A write"))
        self.assertFalse(is_attempt_ask("track A write"))
        self.assertEqual(parse_problem(ask="track A write"), "A")
        self.assertEqual(parse_problem(problem="A"), "A")
        self.assertTrue(is_proof_ask("RH proof chain please"))
        self.assertTrue(is_proof_ask("RH"))
        self.assertFalse(is_proof_ask(""))
        self.assertFalse(is_proof_ask("now what"))
        self.assertEqual(parse_problem(ask="RH proof chain please"), "RH")
        ym_b = "Yang mills and bad can you finish those for me please"
        self.assertTrue(is_proof_ask(ym_b))
        self.assertEqual(parse_problems(ask=ym_b), ["NS", "YM"])
        self.assertEqual(parse_problem(problem="YM"), "YM")
        self.assertTrue((ROOT / "docs" / "YM-PROOF-CHAIN.md").is_file())
        ym = run(out=Path(tempfile.mkdtemp()) / "da_proof_ym.json", problem="YM")
        self.assertEqual(ym["problem"], "YM")
        self.assertEqual(ym["counts"]["write"], 1)
        self.assertEqual(parse_problem(ask="Xavier Stokes"), "NS")
        rh = run(out=Path(tempfile.mkdtemp()) / "da_proof_rh.json", problem="RH")
        self.assertEqual(rh["problem"], "RH")
        self.assertIn("1/2", rh["theorem"]["aimed"])
        self.assertTrue(any("inverse-GCD" in line for line in rh["object"]["window"]))
        paper_ask = "use my best paper and write RH please"
        self.assertTrue(is_proof_ask(paper_ask))
        self.assertFalse(is_attempt_ask(paper_ask))
        self.assertEqual(parse_problem(ask=paper_ask), "RH")
        paper = run(
            out=Path(tempfile.mkdtemp()) / "da_proof_rh_paper.json",
            problem="",
            ask=paper_ask,
        )
        self.assertEqual(paper["picked"], ["RH"])
        self.assertIsNotNone(paper["chains"][0]["best_paper"])
        self.assertEqual(paper["chains"][0]["best_paper"]["slot"], "Q")
        self.assertTrue(any("Theorem P" in row for row in paper["chains"][0]["best_paper"]["sits"]))
        a = run(out=Path(tempfile.mkdtemp()) / "da_proof_a.json", problem="A")
        self.assertEqual(a["problem"], "A")
        self.assertTrue(a["chains"][0]["this_pde_complete"])
        self.assertIn("this PDE", a["theorem"]["aimed"])
        self.assertEqual(a["lines"][5]["status"], "have")
        self.assertEqual(a["lines"][6]["status"], "write")
        both = run(out=Path(tempfile.mkdtemp()) / "da_proof_both.json", problem="", ask=both_ask)
        self.assertEqual(both["picked"], ["NS", "A"])
        self.assertEqual(len(both["chains"]), 2)
        self.assertEqual(
            set(PROBLEMS),
            {"NS", "A", "RH", "YM", "BSD", "HODGE", "POINCARE", "PNP"},
        )
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))
        self.assertTrue((ROOT / "docs" / "DA-PROOF.md").is_file())
        self.assertTrue((ROOT / "docs" / "NS-PROOF-CHAIN.md").is_file())
        self.assertTrue((ROOT / "docs" / "A-PROOF-CHAIN.md").is_file())
        self.assertTrue((ROOT / "docs" / "THEOREM-A-DEPOSIT.md").is_file())
        self.assertIn("Not classical", (ROOT / "docs" / "THEOREM-A-DEPOSIT.md").read_text())
        self.assertTrue((ROOT / "tex" / "theorem-a-q1.tex").is_file())
        tex = (ROOT / "tex" / "theorem-a-q1.tex").read_text()
        self.assertIn("Theorem A", tex)
        self.assertIn("Not classical NS", tex)
        self.assertIn("this PDE only", tex)
        self.assertTrue((ROOT / "docs" / "RH-PROOF-CHAIN.md").is_file())
        self.assertTrue((ROOT / "docs" / "YM-PROOF-CHAIN.md").is_file())
        self.assertTrue((ROOT / "docs" / "BSD-PROOF-CHAIN.md").is_file())
        self.assertTrue((ROOT / "docs" / "HODGE-PROOF-CHAIN.md").is_file())
        self.assertTrue((ROOT / "docs" / "POINCARE-PROOF-CHAIN.md").is_file())
        self.assertTrue((ROOT / "docs" / "PNP-PROOF-CHAIN.md").is_file())
        self.assertTrue((ROOT / "docs" / "DA-COMPLETE.md").is_file())
        self.assertTrue(is_proof_ask("Please write BSD"))
        self.assertEqual(parse_problem(ask="Please write BSD"), "BSD")
        self.assertEqual(parse_problem(problem="BSD"), "BSD")
        bsd = run(out=Path(tempfile.mkdtemp()) / "da_proof_bsd.json", problem="BSD")
        self.assertEqual(bsd["problem"], "BSD")
        self.assertEqual(bsd["counts"]["write"], 1)
        self.assertIn("r_an", bsd["theorem"]["aimed"])
        framework = (
            "file:///var/mobile/Library/SMS/Attachments/ee/14/"
            "71395E22-293F-49C5-835C-56CA5C63EE8F/BSD_SPECTRAL_FRAMEWORK.pdf"
        )
        self.assertTrue(is_proof_ask(framework))
        self.assertTrue(is_proof_ask("spectral framework"))
        self.assertFalse(is_attempt_ask(framework))
        self.assertEqual(parse_problem(ask=framework), "BSD")
        self.assertEqual(parse_problem(ask="spectral framework"), "BSD")
        seated = run(
            out=Path(tempfile.mkdtemp()) / "da_proof_bsd_paper.json",
            problem="",
            ask=framework,
        )
        self.assertEqual(seated["picked"], ["BSD"])
        paper = seated["chains"][0]["best_paper"]
        self.assertIsNotNone(paper)
        self.assertEqual(paper["slot"], "Q")
        self.assertTrue(any("1/gcd" in row for row in paper["sits"]))
        self.assertTrue(any("retracted" in row for row in paper["false"]))
        self.assertIn("not BSD line (6)", paper["not"])
        finish_b = "Please finish bad for me please. So I can complete proof chain"
        self.assertTrue(is_proof_ask(finish_b))
        self.assertFalse(is_attempt_ask(finish_b))
        self.assertEqual(parse_problems(ask=finish_b), ["NS"])
        finished = run(
            out=Path(tempfile.mkdtemp()) / "da_proof_finish_b.json",
            problem="",
            ask=finish_b,
        )
        self.assertEqual(finished["picked"], ["NS"])
        comp = finished["chains"][0]["completion"]
        self.assertEqual(comp["done"], [1, 2, 3, 4, 5])
        self.assertEqual(comp["not_done"], [6])
        self.assertEqual(comp["waiting"], [7, 8, 9])
        self.assertFalse(comp["leftover_sits"])
        self.assertTrue(comp["emit_is_not_finish"])
        self.assertEqual(finished["lines"][5]["status"], "write")
        phone_final = (
            "file:///var/mobile/Library/SMS/Attachments/30/00/"
            "8D36CC33-3B6B-4C40-9C63-2F60AA8DCCB6/BSD%20final.pdf"
        )
        self.assertTrue(is_proof_ask(phone_final))
        self.assertTrue(is_proof_ask("BSD final"))
        self.assertFalse(is_attempt_ask(phone_final))
        self.assertEqual(parse_problem(ask=phone_final), "BSD")
        final = run(
            out=Path(tempfile.mkdtemp()) / "da_proof_bsd_final.json",
            problem="",
            ask=phone_final,
        )
        self.assertEqual(final["picked"], ["BSD"])
        self.assertTrue(
            any("BSD final.pdf" in row for row in final["chains"][0]["best_paper"]["false"])
        )
        self.assertIn("not Hodge", final["chains"][0]["best_paper"]["not"])
        hodge_ask = (
            "Hodge conjecture? file:///var/mobile/Library/SMS/Attachments/"
            "30/00/8D36CC33-3B6B-4C40-9C63-2F60AA8DCCB6/BSD%20final.pdf"
        )
        self.assertTrue(is_proof_ask(hodge_ask))
        self.assertTrue(is_proof_ask("Hodge conjecture?"))
        self.assertFalse(is_attempt_ask(hodge_ask))
        self.assertEqual(parse_problems(ask=hodge_ask), ["HODGE", "BSD"])
        self.assertEqual(parse_problem(problem="HODGE"), "HODGE")
        both = run(
            out=Path(tempfile.mkdtemp()) / "da_proof_hodge.json",
            problem="",
            ask=hodge_ask,
        )
        self.assertEqual(both["picked"], ["HODGE", "BSD"])
        self.assertEqual(both["chains"][0]["problem"], "HODGE")
        self.assertEqual(both["chains"][0]["lines"][5]["status"], "write")
        self.assertIsNone(both["chains"][0].get("best_paper"))
        self.assertIn("H^{p,p}", both["theorem"]["aimed"])
        self.assertTrue(is_proof_ask("Smoothness and existence"))
        self.assertEqual(parse_problem(ask="Smoothness and existence"), "NS")
        self.assertTrue(is_proof_ask("point care conjecture"))
        self.assertEqual(parse_problem(ask="point care conjecture"), "POINCARE")
        self.assertTrue(is_proof_ask("P versus NP"))
        self.assertEqual(parse_problem(ask="P versus NP"), "PNP")
        self.assertFalse(is_attempt_ask("P versus NP"))
        poincare = run(
            out=Path(tempfile.mkdtemp()) / "da_proof_poincare.json",
            problem="POINCARE",
        )
        self.assertTrue(poincare["chains"][0]["literature_complete"])
        self.assertTrue(poincare["chains"][0]["completion"]["leftover_sits"])
        self.assertEqual(poincare["chains"][0]["completion"]["not_done"], [])
        self.assertIsNone(poincare["write_n"])
        pnp = run(out=Path(tempfile.mkdtemp()) / "da_proof_pnp.json", problem="PNP")
        self.assertEqual(pnp["write_n"], 5)
        self.assertFalse(pnp["chains"][0]["completion"]["leftover_sits"])
        letter = (
            "Smoothness and existence. point care conjecture. "
            "one on Zeta. P versus NP. SFE interpretation."
        )
        self.assertEqual(
            parse_problems(ask=letter),
            ["NS", "RH", "POINCARE", "PNP"],
        )
        exam = (
            "Please write the final, corrected and complete versions "
            "using DA and cursor please. This is to test the DA's ability "
            "to understand and finish or assist in closing proof chains"
        )
        self.assertTrue(is_all_ask(ask=exam))
        self.assertTrue(is_proof_ask(exam))
        self.assertFalse(is_attempt_ask(exam))
        self.assertEqual(parse_problems(ask=exam), list(PROBLEMS))
        dumped = run(
            out=Path(tempfile.mkdtemp()) / "da_proof_all.json",
            problem="ALL",
            ask=exam,
        )
        self.assertEqual(dumped["picked"], list(PROBLEMS))
        self.assertTrue(dumped["meta"]["complete_is_not_qed"])
        self.assertEqual(dumped["meta"]["writeup"], "docs/DA-COMPLETE.md")
        by_p = {c["problem"]: c for c in dumped["chains"]}
        self.assertEqual(by_p["NS"]["lines"][5]["status"], "write")
        self.assertTrue(by_p["POINCARE"]["completion"]["leftover_sits"])
        self.assertTrue(by_p["A"]["this_pde_complete"])
        self.assertFalse(by_p["BSD"]["completion"]["leftover_sits"])
        bsd_doc = (ROOT / "docs" / "BSD-PROOF-CHAIN.md").read_text()
        self.assertIn("Documented, 5 September 2026", bsd_doc)
        self.assertIn("DA did **not**", bsd_doc)
        self.assertIn("complete leftover (6)", bsd_doc)
        millennial = "Give me a master status report on all of the millennium proof chains"
        self.assertTrue(is_all_ask(ask=millennial))
        self.assertEqual(parse_problems(ask=millennial), list(PROBLEMS))
        mps = "present to me all of the MP's on status report"
        self.assertTrue(is_all_ask(ask=mps))
        self.assertEqual(parse_problems(ask=mps), list(PROBLEMS))
        self.assertTrue(is_proof_ask(millennial))
        hodge_sfe = "Resolution of the Hodge Conjecture via the Simons Field Equation (SFE)"
        self.assertTrue(is_proof_ask(hodge_sfe))
        self.assertEqual(parse_problems(ask=hodge_sfe), ["HODGE"])
        rh_doc = (ROOT / "docs" / "RH-PROOF-CHAIN.md").read_text()
        self.assertIn("Documented, 5 September 2026", rh_doc)
        self.assertIn("There is **no**", rh_doc)
        self.assertIn("completed RH", rh_doc)
        hodge_doc = (ROOT / "docs" / "HODGE-PROOF-CHAIN.md").read_text()
        self.assertIn("enclosed letter", hodge_doc)
        self.assertIn("Lemma 1 builds the close", hodge_doc)
        self.assertIn("C18", hodge_doc)


if __name__ == "__main__":
    unittest.main()
