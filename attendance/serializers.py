# attendance/serializers.py

from rest_framework import serializers
from .models import Attendance
from students.serializers import StudentSerializer # Student ki details dikhane ke liye
from students.models import Student # Is line ko add karo

class AttendanceSerializer(serializers.ModelSerializer):
    # Hum student ki poori details dikhana chahte hain, na ki sirf ID.
    # 'read_only=True' ka matlab hai ki response me student ki details dikhengi.
    student_details = StudentSerializer(source='student', read_only=True)

    # 'write_only=True' ka matlab hai ki naya record banate time hum sirf student ki ID bhejenge.
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), write_only=True)

    class Meta:
        model = Attendance
        # Ye saari fields API me istemaal hongi
        fields = ['id', 'student', 'student_details', 'date', 'present']