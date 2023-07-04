from django.test import SimpleTestCase
from libs.misc import convert_excel_number_to_date
from datetime import datetime

class ConvTest(SimpleTestCase):
  """Conversion Test"""

  def test_anynumber(self):
    result = convert_excel_number_to_date(41941)

    self.assertEqual(result, datetime(2014, 10, 29).date())
  
  def test_zero(self):
    result = convert_excel_number_to_date(0)

    self.assertNotEqual (result, datetime(1900, 1, 1).date())