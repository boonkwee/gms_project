import os
import openpyxl
import random
import datetime
from pprint import pprint
from django.test import SimpleTestCase, TestCase
from guests.models import person_type, hotel_guest
from gqf.models import GQF
from gms.models import guest_transaction
from sheets.record import GuestRecord, ReservationRecord
from libs.misc import running_test, convert_excel_number_to_date
from custom_functions.apps import queryset_label_to_reverse_dict


class SheetTest(TestCase):
  file = os.path.join(os.getcwd(), 'test', 'test_3rows.xlsx')
  test_record = {
      'NRIC'                        : 'S0000000E',
      'Name of PUQ'                 : 'Ali Mohd',
      'Community Dweller \n(Y/N) '  : 'Yes',
      'Date of Birth'               : datetime.date(day=13, month=6, year=2003),
      'QO Start Date'               : convert_excel_number_to_date(41991),
      'QO End Date'                 : datetime.date(day=13, month=6, year=2023),
      'Facility'                    : GQF.objects.get(code='VHAC-A', enabled=True),
    }
  field_names = [
    'guest_id',
    'guest_name',
    'guest_comm_dweller',
    'guest_date_of_birth',
    'trans_guest_id',
    'trans_date_checkin_planned',
    'trans_date_checkout_planned',
    'trans_checkin_hotel',
  ]

  def setUp(self):
    guest_type = person_type.objects.create(guest_type='Guest')
    gqf = GQF.objects.create(code='VHAC-A', enabled=True)
    if os.path.exists(self.file):
      self.load_data()
      self.selected_index = random.choice(list(range( len(self.file_data) -1 ))) +1
    else:
      raise IOError(f'test data file: [{self.file}] missing')
    return super().setUp()

  def __init__(self, methodName: str = "runTest"):
    super().__init__(methodName)


  def test_file_exist(self):
    self.assertTrue(os.path.exists(self.file))


  def load_data(self):
    wb = openpyxl.load_workbook(self.file)
    sheet = wb.active
    
    self.file_data = []
    for row in sheet.rows:
      line = [c.value if c.value is not None else '' for c in row]
      if any(line):                
        self.file_data.append(line)
    self.file_headers = tuple(self.file_data[0])
    self.file_data = self.file_data[1:]
  

  def test_guest_type(self):
    g = person_type.objects.get(guest_type='Guest')
    self.assertEqual(g.guest_type, 'Guest')


  def test_gqf(self):
    g = GQF.objects.get(code='VHAC-A', enabled=True)
    self.assertIsNotNone(g)
  

  def isReservationRecDict(self):
    data_dict = dict(zip(self.file_headers, self.file_data[self.selected_index]))
    g = ReservationRecord(data_dict=data_dict)
    # print('Reservation Record')
    # pprint(g.object)
    self.assertTrue(isinstance(g.object_record, dict))


  def isGuestRecDict(self):
    data_dict = dict(zip(self.file_headers, self.file_data[self.selected_index]))
    g = GuestRecord(data_dict=data_dict)
    # print('Guest Record')
    # pprint(g.object)
    self.assertTrue(isinstance(g.object_record, dict))


  def test_guest_record(self):
    g = GuestRecord(data_dict=self.test_record)
    self.assertIsNotNone(g)
    guest = g.object
    reservation = guest_transaction.objects.get(trans_guest_id=self.test_record['NRIC'])
    self.assertIsNotNone(reservation)
    self.assertEquals(reservation.trans_date_checkin_planned, self.test_record['QO Start Date'])
    guest_record_dict = g.record_fields
    for column_name, field_value in [c_name for c_name in self.test_record.items() if c_name in guest_record_dict]:
      field_name = guest_record_dict[column_name]
      field = guest._meta.get_field(field_name)
      field_type = field.get_internal_type()
      print(field_type)
      if field_type == 'BooleanField':
        LHS = 'YES' if getattr(guest, field_name) else 'NO'
      else:
        LHS = getattr(guest, field_name)
      if field_type == 'DateField':
        RHS = field_value
      else:
        RHS = field_value.upper()
      self.assertEquals(LHS, RHS)


  def test_reservation_record(self):
    r = ReservationRecord(data_dict=self.test_record)
    # print(r.object.trans_date_checkin_planned)
    self.assertIsNotNone(r)
    reservation = r.object
    reservation_record_dict = r.record_fields
    for column_name, field_value in [c_name for c_name in self.test_record.items() if c_name in reservation_record_dict]:
      field_name = reservation_record_dict[column_name]
      field = reservation._meta.get_field(field_name)
      field_type = field.get_internal_type()
      print(field_type)
      if field_type == 'BooleanField':
        LHS = 'YES' if getattr(reservation, field_name) else 'NO'
      else:
        LHS = getattr(reservation, field_name)
        
      if field_type == 'DateField':
        RHS = field_value
      else:
        RHS = field_value.upper()
      self.assertEquals(LHS, RHS)


  def test_guest_record_exception_missing_fields(self):
    compulsory_fields = GuestRecord.compulsory_fields
    for f in self.test_record:
      test_record = dict(self.test_record)
      if f  in compulsory_fields:
        del test_record[f]
        self.assertRaises(ValueError, GuestRecord, test_record)
      else:
        self.assertNotIn(f, compulsory_fields)

  def test_reservation_record_exception_missing_fields(self):
    compulsory_fields = ReservationRecord.compulsory_fields
    for f in self.test_record:
      test_record = dict(self.test_record)
      if f in compulsory_fields:
        del test_record[f]
        self.assertRaises(ValueError, ReservationRecord, test_record)
      else:
        self.assertNotIn(f, compulsory_fields)

  def test_iterTest(self):
    self.isGuestRecDict()
    self.isReservationRecDict()    

  def test_reservation_double_entry(self):
    for i in range(len(self.file_data)):
      data_dict = dict(zip(self.file_headers, self.file_data[i]))
      g = GuestRecord(data_dict)
    g = GuestRecord(data_dict=self.test_record)
    g = GuestRecord(data_dict=self.test_record)
    self.assertEquals(hotel_guest.objects.all().count(), len(self.file_data) + 1)
    self.assertEquals(guest_transaction.objects.all().count(), len(self.file_data) + 1)