from django.db import models

class SensorData(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    light = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

class DeviceState(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)  # Điều này sẽ tạo giá trị timestamp tự động với thời gian hiện tại khi tạo mới
    light = models.BooleanField(default=False)
    fan = models.BooleanField(default=False)
    ac = models.BooleanField(default=False)

    def __str__(self):
        return f"DeviceState at {self.timestamp}"