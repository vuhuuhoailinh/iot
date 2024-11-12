from rest_framework import serializers
from .models import SensorData
from .models import DeviceState

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = ['temperature', 'humidity', 'light', 'timestamp']

class DeviceStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceState
        fields = ['light', 'fan', 'ac', 'timestamp']
