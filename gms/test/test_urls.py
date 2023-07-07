from django.test import SimpleTestCase
from django.urls import reverse, resolve
from libs.misc import running_test
from gms import views


class TestUrls(SimpleTestCase):
  def test_reservations_url_is_resolved(self):
    url = reverse('reservations')
    self.assertEquals(resolve(url).func.view_class, views.ReservationListView)
  
  def test_resolving_checkin_url(self):
    url = reverse('process-check-in')
    self.assertEquals(resolve(url).func, views.process_checkin)

  def test_resolving_checkin_url(self):
    url = reverse('process-check-out')
    self.assertEquals(resolve(url).func, views.process_checkout)

  def test_resolving_upload_url(self):
    url = reverse('upload')
    self.assertEquals(resolve(url).func, views.upload)
  
  def test_resolving_upload_details(self):
    url = reverse('upload_details')
    self.assertEquals(resolve(url).func, views.manual_ingest)

  def test_resolving_dashboard(self):
    url = reverse('dashboard')
    self.assertEquals(resolve(url).func, views.dashboard)

  def test_resolving_search(self):
    url = reverse('search')
    self.assertEquals(resolve(url).func, views.search_checkin)