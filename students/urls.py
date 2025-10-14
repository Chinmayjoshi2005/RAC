# students/urls.py

from django.urls import path
# StudentDetail ko yahan import karo
from .views import StudentListCreate, StudentDetail

urlpatterns = [
    # Ye URL poori list ke liye hai (GET, POST)
    path('students/', StudentListCreate.as_view(), name='student-list-create'),
    # YEH NAYA URL HAI: Ye ek single student ke liye hai (GET, PUT, DELETE)
    # <int:pk> ka matlab hai ki yahan student ki ID (ek number) aayegi
    path('students/<int:pk>/', StudentDetail.as_view(), name='student-detail'),
]