from django import forms
from .models import guest_transaction
from django.forms import ModelForm

# https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/#selecting-the-fields-to-use
class ReservationForm(ModelForm):
    class Meta:
        model = guest_transaction
        fields = '__all__'