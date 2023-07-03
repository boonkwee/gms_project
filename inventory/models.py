from django.db import models
import uuid
from gqf.models import GQF

# Create your models here.
class suite_type(models.Model):
  # hotel = models.ForeignKey("gqf", on_delete=models.RESTRICT)
  suite_type = models.CharField(primary_key=True, max_length=40,
                                verbose_name='Suite Type',
                                db_column='suite_type')
  
  description = models.CharField(max_length=255, blank=True, null=True,
                                  verbose_name='Description',
                                  db_column='description')
  
  sortorder = models.IntegerField(default=0,
                                  verbose_name='Sort order',
                                  db_column='sortorder',
                                  db_comment='For sorting and display purpose')
  
  modified = models.DateTimeField(auto_now=True, verbose_name="Modified")
  created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
  
  class Meta:
    db_table = "tbl_cbk_suite_type"
    ordering = ('sortorder', )
  
  def __str__(self):
    return self.suite_type

class inventory_status(models.Model):
  status = models.CharField(primary_key=True, max_length=40,
                            verbose_name='Room Status',
                            db_column='status')
  description = models.CharField(max_length=80, null=True, blank=True,
                                  verbose_name='Description',
                                  db_column='description')
  value = models.IntegerField(default=99,
                              db_comment='For sorting and display purpose')
  modified = models.DateTimeField(auto_now=True, verbose_name="Modified")
  created = models.DateTimeField(auto_now_add=True, verbose_name="Created")

  class Meta:
    db_table = "tbl_cbk_inventory_status"
    ordering = ("value",)
  
  def __str__(self):
    return self.status

class room(models.Model):
  room_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                              verbose_name='Room ID',
                              db_column='room_id')
  
  room_type = models.ForeignKey(suite_type, on_delete=models.RESTRICT,
                                verbose_name='Suite Type',
                                db_column='room_type')
  
  room_hotel = models.ForeignKey(GQF, on_delete=models.CASCADE,
                                  verbose_name='Facility Name',
                                  db_column='room_hotel')
  
  room_name = models.CharField(max_length=80,
                                blank=False, null=False,
                                verbose_name='Room Name',
                                db_column='room_name')
  
  room_twinroom = models.BooleanField(default=False,
                                      verbose_name='Twin Room',
                                      db_column='room_twinroom')
  
  room_status = models.ForeignKey(inventory_status, on_delete=models.DO_NOTHING,
                                  verbose_name='Room Status',
                                  db_column='room_status')
  
  room_modified = models.DateTimeField(auto_now=True, verbose_name="Modified")
  room_created = models.DateTimeField(auto_now_add=True, verbose_name="Created")

  class Meta:
    db_table = "tbl_cbk_room_inventory"
    models.UniqueConstraint(fields=["room_type", "room_hotel"], name="unique_models")
  
  def __str__(self):
    suffix = f' ({self.room_status})' if f'{self.room_status}' == 'Available' else ''
    return f'{self.room_name}-{self.room_hotel}' + suffix
