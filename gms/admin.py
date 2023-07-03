from typing import Any, Optional
from django import forms
from django.contrib import admin
from django.db.models.fields.related import ForeignKey
from django.forms.models import ModelChoiceField
from django.http.request import HttpRequest
from .models import guest_transaction
from inventory.models import room, inventory_status
from django.contrib.sessions.models import Session

# Register your models here.
class ReservationCreationForm(forms.ModelForm):
    class Meta:
        model = guest_transaction
        fields = '__all__'
        exclude = ('transaction_id', )

class ReservationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in guest_transaction._meta.fields]
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'trans_room_id':
            kwargs['queryset'] = room.objects.filter(room_status='Available')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    form = ReservationCreationForm
    def save_model(self, request, obj, form, change):
        room_selected = obj.trans_room_id
        if room_selected and room_selected.room_status == 'Available':
            room_selected.room_status = 'Reserved'
            room.save()
            obj.trans_checkin_hotel = room_selected.room_hotel
        if room_selected is None:
            obj.trans_checkin_hotel = None

        super().save_model(request, obj, form, change)

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', 'expire_date']
    readonly_fields = ['session_key', 'session_data', 'expire_date']

admin.site.register(Session, SessionAdmin)
admin.site.register(guest_transaction, ReservationAdmin)
admin.site.site_header = "GMS Administration"
