from django.db import models


# Create your models here.

class Student(models.Model):
    roll_no = models.IntegerField(primary_key=True)
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=20)
    email = models.CharField(max_length=30, unique=True)
    total_attendance_percentage = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.roll_no) + ' ' + self.f_name
