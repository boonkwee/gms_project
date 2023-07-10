from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from .models import SystemUser
from .forms import CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()



# Register your models here.
# class SysUserAdmin(admin.ModelAdmin):
class SysUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    # list_display = ('username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active',
    #                 'password_expiry_date')
    # fields = ('username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active',
    #           'password_expiry_date')
    # readonly_fields = ['password']
    list_filter = [field.name for field in SystemUser._meta.fields if not field.primary_key and not field.name=="password"]

    def can_view_hotel(self, hotel):
        if self.groups.filter(name='OpsCen').exists():
            return True
        return self.associated_hotels.filter(name=hotel).exists()

    def clean(self):
        super().clean()
        if self.groups.filter(name='DM').exists() and not self.associated_hotels.exists():
            raise ValidationError("Users in 'DM' group must have at least one associated hotel.")

    def save_model(self, request, obj, form, change):
        # Hash the password if it's provided
        if form.cleaned_data.get('password'):
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)


admin.site.register(SystemUser, SysUserAdmin)