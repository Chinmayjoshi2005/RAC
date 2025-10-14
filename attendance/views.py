# attendance/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Attendance
from students.models import Student
from .serializers import AttendanceSerializer
from datetime import date

class AttendanceListCreate(generics.ListCreateAPIView):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        query_date_str = self.request.query_params.get('date', None)
        if query_date_str:
            query_date = date.fromisoformat(query_date_str)
            return Attendance.objects.filter(date=query_date)
        return Attendance.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student = serializer.validated_data.get('student')
        date = serializer.validated_data.get('date')
        present = serializer.validated_data.get('present')

        # YEH LINE BUG KO FIX KARTI HAI:
        # Agar record mil gaya to update karo, nahi to naya bana do.
        instance, created = Attendance.objects.update_or_create(
            student=student,
            date=date,
            defaults={'present': present}
        )

        response_serializer = self.get_serializer(instance)
        headers = self.get_success_headers(response_serializer.data)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK

        return Response(response_serializer.data, status=status_code, headers=headers)

class BulkAttendanceView(APIView):
    def post(self, request, *args, **kwargs):
        date_str = request.data.get('date')
        student_ids = request.data.get('student_ids', [])
        is_present = request.data.get('present', True)

        if not date_str or not student_ids:
            return Response({'error': 'Date and student_ids are required.'}, status=status.HTTP_400_BAD_REQUEST)

        attendance_date = date.fromisoformat(date_str)

        for student_id in student_ids:
            try:
                student = Student.objects.get(id=student_id)
                Attendance.objects.update_or_create(
                    student=student,
                    date=attendance_date,
                    defaults={'present': is_present}
                )
            except Student.DoesNotExist:
                pass 

        return Response({'status': 'success'}, status=status.HTTP_200_OK)