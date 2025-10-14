# students/views.py

from rest_framework import generics
from .models import Student
from .serializers import StudentSerializer

# Ye view students ki list dikhayega aur naye student create karega (ye pehle se tha)
class StudentListCreate(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

# YEH NAYA VIEW HAI: Ye ek single student ko dekhega, update karega ya delete karega
class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer