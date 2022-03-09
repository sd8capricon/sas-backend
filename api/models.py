from pyexpat import model
from django.db import models

# Create your models here.


class Student(models.Model):
    roll_no = models.IntegerField(primary_key=True, unique=True)
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=20)
    email = models.CharField(max_length=30, unique=True, null=True)
    total_attendance_percentage = models.FloatField(null=True)

    def __str__(self):
        return str(self.roll_no) + " " + self.f_name


class Teacher(models.Model):
    teacher_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=50)
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.teacher_id) + " " + self.f_name


class Course(models.Model):
    course_id = models.BigAutoField(primary_key=True)
    course_name = models.CharField(max_length=20)
    taught_by = models.OneToOneField(
        Teacher, null=True, on_delete=models.SET_NULL)
    enrolled_students = models.ManyToManyField(Student, null=True)

    def __str__(self):
        return str(self.course_id) + " " + self.course_name


class Attendance(models.Model):
    date = models.DateTimeField(auto_now=True)
    student_status = models.BooleanField(null=True)
    lec_no = models.IntegerField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.student)

class Lec_Stat(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lec_no = models.IntegerField()
    students_present = models.IntegerField()

    def __str__(self):
        return str(self.course_id) + str(self.lec_no) + str(self.students_present)
