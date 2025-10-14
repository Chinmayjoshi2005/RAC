# students/models.py

from django.db import models

# Ye hamara Student ka blueprint hai
class Student(models.Model):
    student_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # Hum baad me aur bhi cheezein add kar sakte hain, jaise photo, class, etc.

    def __str__(self):
        return self.name