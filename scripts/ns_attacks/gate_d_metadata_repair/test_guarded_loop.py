import unittest, tempfile, json, subprocess, sys
from pathlib import Path
from unittest.mock import patch
import gaussian_gate_d_with_sidecar as g
class Tests(unittest.TestCase):
 def test_no_exploratory_signed_call(self):
  with tempfile.TemporaryDirectory() as d:
   args=type("Args",(),dict(n=24,L=12.,c=200.,s_end=.01,ds=.01,
       log_every=1,high_fraction=.5,signed_K=1,signed_N=6,
       safe_sidecar=True,output=str(Path(d)/"log.jsonl")))()
   with patch.object(g,"signed_diagnostics",side_effect=AssertionError("exploratory evaluator called")):
    g.run(args)
   rows=[json.loads(x) for x in Path(args.output).read_text().splitlines()][1:]
   self.assertEqual(len(rows),2)
   for row in rows:
    self.assertEqual(row["diagnostic_status"],"sign_unverified")
    self.assertIsNone(row["T_sc"])
    self.assertIsNone(row["D"])
    self.assertFalse(row["safe_signed"]["crossing_certified"])
 def test_step_unchanged(self):
  import inspect,gaussian_gate_d
  self.assertEqual(inspect.getsource(g.step),inspect.getsource(gaussian_gate_d.step))
if __name__=="__main__":unittest.main()
