import unittest,tempfile,json
from pathlib import Path
import gaussian_gate_d_with_sidecar as g
class Tests(unittest.TestCase):
 def test_metadata_is_not_certificate(self):
  with tempfile.TemporaryDirectory() as d:
   args=type("Args",(),dict(n=24,L=12.,c=200.,s_end=.01,ds=.01,log_every=1,high_fraction=.5,signed_K=1,signed_N=6,safe_sidecar=True,output=str(Path(d)/"log.jsonl")))()
   g.run(args)
   rows=[json.loads(x) for x in Path(args.output).read_text().splitlines()]
   meta=rows[0]["metadata"]
   self.assertTrue(meta["T_sc_code_available"])
   self.assertFalse(meta["accepted_T_sc_verified"])
   self.assertFalse(meta["accepted_D_verified"])
   self.assertFalse(meta["crossing_certified"])
   for row in rows[1:]:
    self.assertIsNone(row["T_sc"])
    self.assertIsNone(row["D"])
if __name__=="__main__":unittest.main()
