from django.apps import AppConfig
from .mqtt_client import mqtt_client  # Import đối tượng mqtt_client từ mqtt_client.py

class SensorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sensor'

    def ready(self):
        # Bắt đầu vòng lặp của MQTT client khi ứng dụng sẵn sàng
        mqtt_client.loop_start()  # Gọi phương thức loop_start() từ mqtt_client để bắt đầu xử lý kết nối
