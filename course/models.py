from django.db import models
from student.models import Student


# Create your models here.
class Course(models.Model):
    course_id = models.BigAutoField(primary_key=True)
    course_name = models.CharField(max_length=20)
    course_sem = models.IntegerField(
        choices=[(2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)])
    # enrolled_students = models.ManyToManyField(Student, null=True)

    def __str__(self):
        return self.course_name
