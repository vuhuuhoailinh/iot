from django.contrib import admin
from .models import DeviceState
from .models import SensorData
# Register your models here.

@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ['temperature', 'humidity', 'light', 'timestamp']

@admin.register(DeviceState)
class DeviceStateAdmin(admin.ModelAdmin):
    list_display = ['light', 'fan', 'ac', 'timestamp']
