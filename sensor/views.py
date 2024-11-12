from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from .models import SensorData
import json
from .serializers import SensorDataSerializer
from .mqtt_client import publish_message
from rest_framework.pagination import PageNumberPagination
from .models import DeviceState
from .serializers import DeviceStateSerializer
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.routers import DefaultRouter  # Import DefaultRouter từ Django REST Framework



# Pagination cho API dữ liệu cảm biến
class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_size_query_param = 'limit'

# API Endpoint: Lấy danh sách dữ liệu cảm biến
class SensorDataList(generics.ListAPIView):
    queryset = SensorData.objects.all().order_by('-timestamp')
    serializer_class = SensorDataSerializer
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['temperature', 'humidity', 'light']  # Lọc theo các trường này
    search_fields = ['temperature', 'humidity', 'light']  # Tìm kiếm theo các trường này
    ordering_fields = ['timestamp', 'temperature', 'humidity', 'light']  # Sắp xếp theo các trường này

# API Endpoint: Nhận dữ liệu MQTT (POST)
@csrf_exempt
@api_view(['POST'])
def mqtt_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sensor_data = SensorData.objects.create(
                temperature=data.get('temperature'),
                humidity=data.get('humidity'),
                light=data.get('light', False)
            )
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return HttpResponseNotAllowed(['POST'])

# HTML View: Trang chính (Home)
def home_view(request):
    # Kiểm tra xem `DeviceState` có ít nhất một bản ghi không. Điều này rất quan trọng để tránh lỗi 404.
    state = get_object_or_404(DeviceState, pk=1)
    return render(request, 'sensor/home.html', {'device_state': state})

def datasensor_view(request):
    return render(request, 'sensor/datasensor.html')

# HTML View: Bật/tắt thiết bị
@csrf_protect
def toggle_device(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    state = get_object_or_404(DeviceState, pk=1)

    device = request.POST.get('device')
    if device not in ['light', 'fan', 'ac']:
        return JsonResponse({'error': 'Invalid device'}, status=400)

    message = ""
    if device == 'light':
        state.light = not state.light
        message = "1"
    elif device == 'fan':
        state.fan = not state.fan
        message = "2"
    elif device == 'ac':
        state.ac = not state.ac
        message = "3"

    state.save()

    try:
        if message:
            publish_message(message)
    except Exception as e:
        return JsonResponse({'error': f'Failed to send MQTT message: {str(e)}'}, status=500)

    return JsonResponse({'light': state.light, 'fan': state.fan, 'ac': state.ac})

class DeviceStateList(generics.ListAPIView):
    queryset = DeviceState.objects.all().order_by('-timestamp')
    serializer_class = DeviceStateSerializer

def action_history_view(request):
    return render(request, 'sensor/actionhistory.html')

def profile_view(request):
    return render(request, 'sensor/profile.html')

class DeviceStateViewSet(viewsets.ModelViewSet):
    queryset = DeviceState.objects.all().order_by('-timestamp')
    serializer_class = DeviceStateSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['light', 'fan', 'ac']  # Các trường có thể lọc
    search_fields = ['light', 'fan', 'ac']  # Các trường có thể tìm kiếm
    ordering_fields = ['timestamp', 'light', 'fan', 'ac']  # Các trường có thể sắp xếp

