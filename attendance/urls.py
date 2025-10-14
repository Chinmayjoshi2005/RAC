# attendance/urls.py

from django.urls import path
from .views import AttendanceListCreate

urlpatterns = [
    path('attendance/', AttendanceListCreate.as_view(), name='attendance-list-create'),
]