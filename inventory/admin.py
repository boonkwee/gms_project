from django.contrib import admin
from .models import room, inventory_status, suite_type

# Register your models here.
class RoomAdmin(admin.ModelAdmin):
    list_display = [field.name for field in room._meta.fields if not field.primary_key]
    list_filter = [field.name for field in room._meta.fields if not field.primary_key]
    search_fields = ['room_hotel', 'room_name', 'room_type']

class SuiteTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in suite_type._meta.fields]

class InventoryStatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in inventory_status._meta.fields]

admin.site.register(room, RoomAdmin)
admin.site.register(inventory_status, InventoryStatusAdmin)
admin.site.register(suite_type, SuiteTypeAdmin)