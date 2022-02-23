from pyexpat import model
from django.db import models

# Create your models here.


class Student(models.Model):
    roll_no = models.BigAutoField(primary_key=True)
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=20)
    percentage_attendance = models.FloatField(null=True)

    def __str__(self):
        return str(self.roll_no) + " " + self.f_name


class Teacher(models.Model):
    teacher_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.teacher_id) + " " + self.f_name


class Course(models.Model):
    course_id = models.BigAutoField(primary_key=True)
    course_name = models.CharField(max_length=20)
    taught_by = models.ForeignKey(Teacher, null=True, on_delete=models.SET_NULL)
    enrolled_students = models.ManyToManyField(Student, null=True)

    def __str__(self):
        return str(self.course_id) + " " + self.course_name


class Attendance(models.Model):
    date = models.DateTimeField(auto_now=True)
    student_status = models.BooleanField(null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.student)