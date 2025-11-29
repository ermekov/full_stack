from django.contrib import admin
from .models import Equipment
# Register your models here.

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("id","name","price_per_day",'available_from', 'created_at')
    search_fields = ("name", "description")
    list_filter = ("available_from",)