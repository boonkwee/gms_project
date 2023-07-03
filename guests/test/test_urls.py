from django.test import SimpleTestCase
from django.urls import reverse, resolve
from libs.misc import running_test
from guests import views


class TestUrls(SimpleTestCase):
  @running_test
  def test_reservations_url_is_resolved(self):
    url = reverse('guests')
    self.assertEquals(resolve(url).func.view_class, views.GuestListView)
  
  def _resolving_checkin_url(self):
    url = reverse('check-in')
    self.assertEquals(resolve(url).func, views.process_checkin)
