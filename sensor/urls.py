from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import DeviceStateViewSet

router = DefaultRouter()
router.register(r'action-history', DeviceStateViewSet, basename='action-history')

urlpatterns = [
    # API endpoints
    path('api/sensor-data/', views.SensorDataList.as_view(), name='sensor-data'),  # API để lấy dữ liệu cảm biến
    path('api/mqtt-data/', views.mqtt_data, name='mqtt-data'),  # Endpoint nhận dữ liệu MQTT (POST)
    path('api/action-history/', views.DeviceStateList.as_view(), name='action-history'),  # Endpoint để lấy danh sách trạng thái của thiết bị
    path('iot/api/', include(router.urls)),

    # HTML Views
    path('home/', views.home_view, name='home'),  # Đường dẫn `/home/` để truy cập giao diện chính
    path('toggle-device/', views.toggle_device, name='toggle_device'),  # Endpoint để bật/tắt thiết bị
    path('datasensor/', views.datasensor_view, name='datasensor'),
    path('actionhistory/', views.action_history_view, name='actionhistory'),  # Trang action history
    path('profile/', views.profile_view, name='profile'),
]