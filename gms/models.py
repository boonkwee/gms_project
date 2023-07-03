from django.db import models
import uuid
from guests.models import hotel_guest, person_type
from inventory.models import room
from gqf.models import GQF

# Create your models here.
class guest_transaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                      verbose_name="Reservation ID",
                                      db_column='transaction_id')
    
    trans_guest_id = models.ForeignKey(hotel_guest, on_delete=models.RESTRICT,
                                       blank=False, null=False, 
                                       verbose_name="Guest ID",
                                       db_column='trans_guest_id')
    
    trans_date_checkin = models.DateTimeField(null=True, blank=True,
                                              verbose_name="Check-in",
                                              db_column='trans_date_checkin')
    
    trans_date_checkin_planned = models.DateField(null=True, blank=True,
                                                  verbose_name="Expected Check-in",
                                                  db_column='trans_date_checkin_planned')
    
    trans_date_checkout = models.DateTimeField(null=True, blank=True,
                                               verbose_name="Check-out",
                                               db_column='trans_date_checkout')
    
    trans_date_checkout_planned = models.DateField(null=True, blank=True,
                                                   verbose_name="Expected Check-out",
                                                   db_column='trans_date_checkout_planned')
    
    trans_room_id = models.ForeignKey(room, on_delete=models.RESTRICT,
                                      blank=True, null=True,
                                      verbose_name="Room ID",
                                      db_column='trans_room_id')
    
    trans_remarks = models.TextField(max_length=8192, null=True, blank=True,
                                     verbose_name="Remarks",
                                     db_column='trans_remarks')
    
    trans_checkin_hotel = models.ForeignKey(GQF, on_delete=models.RESTRICT,
                                            blank=True, null=True,
                                            verbose_name="Facility Name",
                                            db_column='trans_checkin_hotel')
    
    trans_modified = models.DateTimeField(auto_now=True, verbose_name="Modified")
    trans_created = models.DateTimeField(auto_now_add=True, verbose_name="Created")

    class Meta:
        db_table = "tbl_cbk_guest_transaction"
    
    def __str__(self):
        checkin_date = f"{self.trans_date_checkin_planned}" if self.trans_date_checkin_planned is not None else "XXXX-XX-XX"
        hotel_str = str(self.trans_checkin_hotel) if self.trans_checkin_hotel is not None else 'No hotel'
        room_name = self.trans_room_id.room_name if self.trans_room_id is not None else 'No room'
        return f"{(self.trans_guest_id.guest_id if self.trans_guest_id else '()')} (" + checkin_date + ", " + hotel_str + ")"

