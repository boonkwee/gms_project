from django.test import SimpleTestCase
from libs.misc import convert_excel_number_to_date, NRIC_checksum
from datetime import datetime

class ConvTest(SimpleTestCase):
  """Conversion Test"""

  def test_anynumber(self):
    result = convert_excel_number_to_date(41941)

    self.assertEqual(result, datetime(2014, 10, 29).date())
  
  def test_zero(self):
    result = convert_excel_number_to_date(0)

    self.assertNotEqual (result, datetime(1900, 1, 1).date())

  def test_nric_checksum(self):
    self.assertTrue(NRIC_checksum('S7606549G'))
    self.assertFalse(NRIC_checksum('s0000000'))
    self.assertFalse(NRIC_checksum(''))
    self.assertRaises(ValueError, NRIC_checksum, None)
    self.assertRaises(ValueError, NRIC_checksum, 9) # any number