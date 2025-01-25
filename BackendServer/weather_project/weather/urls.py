
from django.urls import path
from .views import save_sensor_data  # Correct import

urlpatterns = [
    path('api/temperature', save_sensor_data, name='save_sensor_data'),
]
