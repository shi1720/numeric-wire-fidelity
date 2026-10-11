import sys,unittest
from pathlib import Path
from fractions import Fraction
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from oracle import loads,dumps,valid,decimal
class OracleTests(unittest.TestCase):
 def test_decimal_integer_type(self):
  self.assertTrue(valid({'type':'integer'},loads('42.0')))
  self.assertFalse(valid({'type':'integer'},True))
  self.assertFalse(valid({'type':'integer'},loads('42.000000000000001')))
 def test_exact_multiple(self):
  s=loads('{"type":"number","multipleOf":0.1}')
  self.assertTrue(valid(s,loads('0.3')))
  self.assertFalse(valid(s,loads('0.30000000000000004')))
 def test_bounds_do_not_round(self):
  s=loads('{"type":"integer","maximum":9223372036854775807}')
  self.assertTrue(valid(s,9223372036854775807))
  self.assertFalse(valid(s,9223372036854775808))
 def test_enum_not_boolean(self):
  self.assertFalse(valid({'type':'number','enum':[1]},True))
 def test_decimal_roundtrip(self):
  for t in ['-1e-324','5e-324','1.7976931348623159e308','0.10000000000000001','-0','9007199254740993']:
   self.assertEqual(loads(t),loads(decimal(loads(t))))
 def test_duplicate_keys(self):
  with self.assertRaises(ValueError):loads('{"x":1,"x":2}')
 def test_schema_loss_witness(self):
  self.assertFalse(valid(loads('{"type":"integer","const":9007199254740993}'),9007199254740992))
if __name__=='__main__':unittest.main()
