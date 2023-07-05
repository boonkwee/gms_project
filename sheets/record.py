from django.core.exceptions import ObjectDoesNotExist
from guests.models import hotel_guest
from gms.models import guest_transaction, person_type
from gqf.models import GQF
from libs.misc import convert_excel_number_to_date
from pprint import pprint

class BaseRecord:
  record_fields = dict()
  # declaration for list of compulsory fields, if the extended class have them
  compulsory_fields = []
  created = True

  def __init__(self, data_dict=None):
    if data_dict is None:
      raise ValueError('No data and column field provided')
    if not isinstance(data_dict, dict):
      raise TypeError('Input data is not of dictionary type')
    
    missing_fields = []

    for compulsory_field in self.compulsory_fields:
      if compulsory_field not in data_dict:
        missing_fields.append(compulsory_field)
    
    if missing_fields:
      # raise ValueError
      raise ValueError(f'Missing compulsory fields: {",".join(missing_fields)}')

    self.fields_in_file = []
    self.object_record = {}
    self.raw_data = {column_name:data_dict[column_name] for column_name in self.record_fields if column_name in self.compulsory_fields}

    for column_name, column_value in data_dict.items():
      if column_name in self.record_fields:
        self.fields_in_file.append(self.record_fields[column_name])
        field_name = self.record_fields[column_name]
        if '_date_' in field_name:
          self.object_record[field_name] = convert_excel_number_to_date(column_value)
          print (f'{field_name} converted to {repr(self.object_record[field_name])}')
        elif field_name == 'guest_comm_dweller':
          self.object_record[field_name] = str(column_value).upper().startswith('Y')
        elif field_name == 'trans_checkin_hotel':
          continue
        else:
          self.object_record[field_name] = column_value


class GuestRecord(BaseRecord):
  record_fields = {
    'NRIC'                      : 'guest_id',
    'Name of PUQ'               : 'guest_name',
    'Community Dweller \n(Y/N) ': 'guest_comm_dweller',
    'Date of Birth'             : 'guest_date_of_birth',
    }
  compulsory_fields = ['NRIC',
                       'Name of PUQ',
                       'Community Dweller \n(Y/N) ',
                       'Date of Birth',
                       ]

  def __init__(self, data_dict=None):
    super().__init__(data_dict)
    reverse_record_fields = {
      value:field
      for field, value in ReservationRecord.record_fields.items()
    }
    all_reservation_fields = {
      field.name:data_dict[reverse_record_fields[field.name]]
      for field in guest_transaction._meta.get_fields() 
      if field.name in ReservationRecord.record_fields.values()
      }
    
    obj_instance = hotel_guest.objects.filter(guest_id=data_dict['NRIC'])

    if obj_instance.exists():
      self.created = False
      self.object = obj_instance
    else:
      self.created = True
      self.object = hotel_guest()

      self.object.guest_type = person_type.objects.get(guest_type='Guest')
      for column_name, column_value in data_dict.items():
        if column_name in self.record_fields:
          field_name = self.record_fields[column_name]
          # field = self.object._meta.get_field(field_name)
          # field_data_type = field.get_internal_type()

          if field_name in ('guest_name', 'guest_id'):
            self.object_record[field_name] = column_value.upper()
          elif field_name == 'guest_comm_dweller':
            self.object_record[field_name] = str(column_value).upper().startswith('Y')

          setattr (self.object, field_name, self.object_record[field_name])
      self.object.save(**all_reservation_fields)


class ReservationRecord(BaseRecord):
  record_fields = {
    'NRIC'          : 'trans_guest_id',
    'QO Start Date' : 'trans_date_checkin_planned',
    'QO End Date'   : 'trans_date_checkout_planned',
    'Facility'      : 'trans_checkin_hotel',
    }
  compulsory_fields = ['NRIC', 'QO Start Date', 'Facility']

  def __init__(self, data_dict=None):
    super().__init__(data_dict)

    # Reservation with Guest ID exists and check-in field is empty
    obj_instance = guest_transaction.objects.filter(
      trans_guest_id=data_dict['NRIC'],
      trans_date_checkin__isnull=True)
    
    if obj_instance.exists():
      self.created = False
      self.object = obj_instance
    else:
      self.created = True
      self.object = guest_transaction()

      for column_name, column_value in data_dict.items():
        if column_name in self.record_fields:
          field_name = self.record_fields[column_name]
          # field = self.object._meta.get_field(field_name)
          # field_data_type = field.get_internal_type()

          if field_name == 'trans_checkin_hotel':
            try:
              facility = GQF.objects.get(code=column_value, enabled=True)
              self.object_record[field_name] = facility
            except GQF.DoesNotExist:
              raise
              
          if field_name == 'trans_guest_id':
              try:
                g = hotel_guest.objects.get(guest_id=column_value.upper())
              except ObjectDoesNotExist:
                GuestRecord(data_dict)
              self.object_record[field_name] = hotel_guest.objects.get(guest_id=column_value.upper())

          setattr (self.object, field_name, self.object_record[field_name])
      self.object.save()