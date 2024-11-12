import paho.mqtt.client as mqtt
from django.conf import settings
import json

# Cấu hình MQTT Broker
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC_CONTROL = "esp8266/led"
MQTT_TOPIC_SENSORS = "esp8266/sensors"

# Khởi tạo MQTT client
mqtt_client = mqtt.Client()

# Hàm xử lý khi kết nối thành công đến broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker successfully!")
        # Đăng ký nhận dữ liệu cảm biến
        client.subscribe(MQTT_TOPIC_SENSORS)
    else:
        print(f"Failed to connect, return code {rc}")

# Hàm xử lý khi nhận được tin nhắn từ broker
def on_message(client, userdata, msg):
    try:
        # Giả sử ESP8266 gửi data dạng JSON
        payload = json.loads(msg.payload.decode('utf-8'))

        # Import trì hoãn model SensorData và DeviceState tại đây
        from .models import SensorData, DeviceState

        # Tạo đối tượng SensorData và lưu dữ liệu vào DB
        sensor_data = SensorData(
            temperature=payload.get('temperature'),
            humidity=payload.get('humidity'),
            light=payload.get('light', False)
        )
        sensor_data.save()

        print("Sensor data saved to database successfully!")

        # Tạo đối tượng DeviceState và lưu trạng thái thiết bị vào DB
        device_state = DeviceState(
            light=payload.get('lightState', False),
            fan=payload.get('fanState', False),
            ac=payload.get('acState', False)
        )
        device_state.save()

        print("Device state saved to database successfully!")

    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON payload: {e}")
    except KeyError as e:
        print(f"Missing key in payload: {e}")
    except Exception as e:
        print(f"Error saving data: {e}")

# Cấu hình các hàm callback
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Kết nối tới MQTT broker
try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
except Exception as e:
    print(f"Failed to connect to MQTT Broker: {e}")

# Hàm để publish tin nhắn đến MQTT broker
def publish_message(message):
    try:
        mqtt_client.publish(MQTT_TOPIC_CONTROL, message)
        print(f"Message published to {MQTT_TOPIC_CONTROL}: {message}")
    except Exception as e:
        print(f"Failed to publish message: {e}")

# Bắt đầu vòng lặp chính 
mqtt_client.loop_start()
