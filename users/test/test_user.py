from django.test import TestCase
from django.contrib.auth import get_user_model
from gqf.models import GQF
from dateutil.relativedelta import relativedelta
from django.utils import timezone

gms_user = get_user_model()
class UserTest(TestCase):
  def setUp(self):
    gqf = GQF.objects.create(code='VHAC-A', enabled=True)
    gqf = GQF.objects.create(code='OHN', enabled=True)

  def test_user_password_expiry(self):
    user = gms_user.objects.create(username='testuser', email='test@email.com', password='12345')
    password_expiry = timezone.now().date() + relativedelta(year=1)
    password_expiry_notification_date = timezone.now().date() + relativedelta(year=1) - relativedelta(weeks=1)
    self.assertEqual(user.password_expiry_date, password_expiry)
    self.assertEqual(user.password_expiry_notification_date, password_expiry_notification_date)
  
  def test_assign_facilities(self):
    user = gms_user.objects.create(username='testuser', email='test@email.com', password='12345')
    associated_facilities = GQF.objects.filter(code__in=['VHAC-A', 'OHN'])
    user.associated_facilities.set(associated_facilities)

    ohn = GQF.objects.get(code='OHN')
    self.assertIsNotNone(ohn)

    has_ohn = user.associated_facilities.filter(code='OHN').exists()
    has_vhac_a = user.associated_facilities.filter(code='VHAC-A').exists()
    donthave_moh = user.associated_facilities.filter(code='MOH').exists()

    self.assertTrue(has_ohn)
    self.assertTrue(has_vhac_a)
    self.assertFalse(donthave_moh)
    self.assertEqual(user.associated_facilities.all().count(), 2)