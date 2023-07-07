from django.test import TestCase
from django.contrib.auth import get_user_model
from dateutil.relativedelta import relativedelta
from django.utils import timezone

gms_user = get_user_model()
class UserTest(TestCase):

  def test_user_password_expiry(self):
    user = gms_user.objects.create(username='testuser', email='test@email.com', password='12345')
    password_expiry = timezone.now().date() + relativedelta(year=1)
    password_expiry_notification_date = timezone.now().date() + relativedelta(year=1) - relativedelta(weeks=1)
    self.assertEqual(user.password_expiry_date, password_expiry)
    self.assertEqual(user.password_expiry_notification_date, password_expiry_notification_date)