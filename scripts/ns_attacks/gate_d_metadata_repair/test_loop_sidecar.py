import json,subprocess,sys,tempfile,unittest
from pathlib import Path
class TestLoop(unittest.TestCase):
 def test_logged_uncertified(self):
  with tempfile.TemporaryDirectory() as d:
   output=Path(d)/'log.jsonl'
   subprocess.run([sys.executable,'gaussian_gate_d_with_sidecar.py','--n','24','--L','12','--signed-K','1','--signed-N','6','--safe-sidecar','--s-end','0.01','--ds','0.01','--output',str(output)],check=True,capture_output=True,text=True)
   rows=[json.loads(x) for x in output.read_text().splitlines()]
   self.assertEqual(len(rows),3)
   for row in rows[1:]:
    self.assertEqual(row['safe_signed']['diagnostic_status'],'sign_unverified')
    self.assertIsNone(row['T_sc']);self.assertIsNone(row['D'])
    self.assertFalse(row['safe_signed']['crossing_certified'])
if __name__=='__main__':unittest.main()
