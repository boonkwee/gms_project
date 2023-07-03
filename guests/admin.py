from django import forms
from django.contrib import admin
from .models import hotel_guest, person_type

# Register your models here.
class PersonTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in person_type._meta.fields]

class HotelGuestCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['guest_location'].initial = 'Facility'

    class Meta:
        model = hotel_guest
        fields = '__all__'
        exclude = ()
    
    guest_location = forms.CharField(label="Current Location", disabled=True)

class GuestAdmin(admin.ModelAdmin):
    form = HotelGuestCreationForm
    list_display = [field.name for field in hotel_guest._meta.fields]
    # list_filter = [field.name for field in hotel_guest._meta.fields]
    search_fields = ['guest_id', 'guest_passport_number', 'guest_name']

admin.site.register(hotel_guest, GuestAdmin)
admin.site.register(person_type, PersonTypeAdmin)