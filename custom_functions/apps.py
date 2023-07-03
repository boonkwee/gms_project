from django.apps import AppConfig, apps
import datetime

DB_COLUMNNAME_TO_FIELDNAME = None
class CustomfunctionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_functions'
    
    def ready(self):
      # DB_COLUMNNAME_TO_FIELDNAME = self.runonce()
      return super().ready()
    
def queryset_label_to_verbose_name(qs_label=''):
  if qs_label == '':
    print('Empty param')
    return ''
  try:
    assert(isinstance(DB_COLUMNNAME_TO_FIELDNAME, dict)) == True
  except NameError:
    print ('DB_COLUMNNAME_TO_FIELDNAME undefined')
    return ''
  except AssertionError:
    print ('DB_COLUMNNAME_TO_FIELDNAME not dictionary')
    return ''
  token = qs_label.split('__')[-1] if '__' in qs_label else qs_label
  print('token: ', token)
  verbose_name = DB_COLUMNNAME_TO_FIELDNAME.get(token)
  return verbose_name if verbose_name else token

def queryset_label_to_verbose_dict():
  print(datetime.datetime.now().isoformat(), ' - Retrieving verbose names...')
  field_verbose = {}
  # Iterate over all registered models
  for model in apps.get_models():
    # Check if the table name starts with 'tbl'
    if model._meta.db_table.startswith('tbl'):
      # Display the model name
      # print(model.__name__)
      
      # Iterate over the field names and verbose names
      for field in [field for field in model._meta.get_fields() if hasattr(field, 'verbose_name')]:
        try:
          field_verbose[field.name] = field.verbose_name
        except AttributeError:
          print(f'{field.name} have no verbose name')
          continue
        # Display the field name and verbose name
        # print(f"Field Name: {field_name}, Verbose Name: {verbose_name}")
  return field_verbose

def queryset_label_to_reverse_dict():
  print(datetime.datetime.now().isoformat(), ' - Retrieving reverse names...')
  field_name_dict = {}
  # Iterate over all registered models
  for model in apps.get_models():
    # Check if the table name starts with 'tbl'
    if model._meta.db_table.startswith('tbl'):
      # Display the model name
      # print(model.__name__)
      
      # Iterate over the field names and verbose names
      for field in [field for field in model._meta.get_fields() if hasattr(field, 'verbose_name')]:
        try:
          field_name_dict[field.verbose_name] = field.name
        except AttributeError:
          print(f'{field.name} have no verbose name')
          continue
        # Display the field name and verbose name
        # print(f"Field Name: {field_name}, Verbose Name: {verbose_name}")
  return field_name_dict
