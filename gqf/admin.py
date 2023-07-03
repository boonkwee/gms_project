from django.contrib import admin
from .models import GQF

# Register your models here.
class GQFAdmin(admin.ModelAdmin):
    list_display = [field.name for field in GQF._meta.fields]
    list_filter =[field.name for field in GQF._meta.fields]

admin.site.register(GQF, GQFAdmin)