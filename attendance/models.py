# attendance/models.py

from django.db import models
# Student model ko import kar rahe hain taaki use jod sakein
from students.models import Student 

class Attendance(models.Model):
    # 'ForeignKey' ka matlab hai ki har attendance record ek Student se juda hua hai.
    # 'on_delete=models.CASCADE' ka matlab hai ki agar koi student delete hota hai,
    # to uska saara attendance record bhi apne aap delete ho jaayega.
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    # 'auto_now_add=True' ka matlab hai ki jab bhi record banega,
    # aaj ki tareekh apne aap save ho jaayegi.
    date = models.DateField()

    # 'BooleanField' status (True ya False) save karega.
    # True = Present, False = Absent
    present = models.BooleanField(default=False)

    class Meta:
        # Ye line सुनिश्चित करती है कि एक student ki ek date par ek hi entry ho.
        unique_together = ('student', 'date')

    def __str__(self):
        # Ye admin panel me record ko aache se dikhayega
        status = "Present" if self.present else "Absent"
        return f"{self.student.name} on {self.date} was {status}"