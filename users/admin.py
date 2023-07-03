from django.contrib import admin
from .models import SystemUser

# Register your models here.
class SysUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active',
                    'password_expiry_date')
    fields = ('username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active',
              'password_expiry_date')
    readonly_fields = ['password']
    list_filter = [field.name for field in SystemUser._meta.fields if not field.primary_key and not field.name=="password"]

    def save_model(self, request, obj, form, change):
        # Hash the password if it's provided
        if form.cleaned_data.get('password'):
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)


admin.site.register(SystemUser, SysUserAdmin)