from django.db import models
from django.forms import widgets
from django.apps import apps
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime

class YesNoWidget(widgets.Select):
    def __init__(self, attrs=None):
        YesNo = [
            (True, 'Yes'),
            (False, 'No'),
        ]
        super().__init__(attrs, YesNo)

class YesNoField(models.BooleanField):
  def __init__(self, *args, **kwargs):
    kwargs['choices'] = [(True, 'Yes'), (False, 'No')]
    kwargs['default'] = True
    super().__init__(*args, **kwargs)

  def formfield(self, **kwargs):
    defaults = {
      'widget': YesNoWidget,
    }
    defaults.update(kwargs)
    return super().formfield(**defaults)
  
  def from_db_value(self, value, expression, connection):
    return self.to_python(value)

  def to_python(self, value):
    return 'Yes' if value else 'No'

  def get_prep_value(self, value):
    return self.to_python(value)

  def value_to_string(self, obj):
    value = self.value_from_object(obj)
    return str(self.to_python(value))

# Create your models here.
class person_type(models.Model):
  guest_type = models.CharField(primary_key=True, max_length=40,
                                verbose_name="Guest Type",
                                db_column='guest_type')
  
  guest_type_description = models.CharField(blank=True, null=True, max_length=80,
                                            verbose_name="Description",
                                            db_column='guest_type_description')
  
  guest_type_sortorder = models.IntegerField(default=0,
                                              verbose_name='Sort Order',
                                              db_column='guest_type_sortorder')
  
  guest_type_modified = models.DateTimeField(auto_now=True, verbose_name="Modified")
  guest_type_created = models.DateTimeField(auto_now_add=True, verbose_name="Created")

  class Meta:
    db_table = "tbl_cbk_guest_type"
    ordering = ('guest_type_sortorder',)

  def __str__(self):
    return self.guest_type

class hotel_guest(models.Model):
  guest_id = models.CharField(primary_key=True, max_length=9,
                              verbose_name="NRIC/ FIN",
                              db_column='guest_id',
                              validators=[MinLengthValidator(9),
                                          MaxLengthValidator(9)])
  
  guest_passport_number = models.CharField(max_length=13, null=True, blank=True,
                                           verbose_name="Passport number",
                                           db_column='guest_passport_number')
  
  guest_name = models.CharField(max_length=80,
                                verbose_name="Guest name",
                                db_column='guest_name')
  
  guest_date_of_birth = models.DateField(verbose_name="Date of Birth",
                                          db_column='guest_date_of_birth')
  
  guest_comm_dweller = YesNoField(default=True, verbose_name="Community Dweller",
                                  db_column='guest_comm_dweller')
  
  guest_type = models.ForeignKey(person_type, on_delete=models.RESTRICT,
                                  verbose_name='Guest Type',
                                  db_column='guest_type')
  
  guest_location = models.CharField(max_length=255, default="Facility",
                                    verbose_name="Current Location",
                                    db_column='guest_location')
  
  guest_modified = models.DateTimeField(auto_now=True, editable=False,
                                        verbose_name="Modified",
                                        db_column='guest_modified')
  
  guest_created = models.DateTimeField(auto_now_add=True,
                                       verbose_name="Created",
                                       db_column='guest_created')

  def __lt__(self, other):
      # Compare based on the guest_id field
      return self.guest_id < other.guest_id

  def __gt__(self, other):
      # Compare based on the guest_id field
      return self.guest_id > other.guest_id

  def get_guest_comm_dweller_display(self):
      return 'Yes' if self.guest_comm_dweller else 'No'

  def clean(self):
      if self.guest_date_of_birth and self.guest_date_of_birth >= timezone.now().date():
          raise ValidationError("Guest date of birth cannot be today or later.")

  class Meta:
      db_table = "tbl_cbk_hotel_guests"

  def save(self, *args, **kwargs):
      # Create a guest_transaction record
      # print(f'Saving {self.guest_id}')
      self.guest_id = self.guest_id.upper()
      self.guest_name = self.guest_name.upper()
      self.clean()
      created = self._state.adding  # Check if the instance is being created or updated
      if self.guest_created is None:
         self.guest_created = timezone.now()
      super().save(*args, **kwargs)  # Save the instance

      # If the instance is being created, create a related guest_transaction record
      if created:
          # print(f'Creating Guest {self.guest_id}')
          guest_transaction = apps.get_model('gms', 'guest_transaction')
          # guest_transaction.objects.create(trans_guest_id=self)
          # guest_transaction.save()
          guest_transaction.objects.update_or_create(trans_guest_id=self)

  def id_only(self):
      return f'{self.guest_id.upper()}'

  def __str__(self):
      # return f'{self.guest_id.upper()}, {self.guest_name.upper()}'
      return f'{self.guest_id.upper()}'
