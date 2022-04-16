from django.db import models


# Create your models here.

class Faculty(models.Model):
    user_types = [
        ('Admin', 'Admin'),
        ('Faculty', 'Faculty')
    ]
    user_id = models.IntegerField(primary_key=True)
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=20, unique=True)
    type = models.CharField(
        max_length=7, choices=user_types, default='Faculty')
    # course_taught = models.ManyToOneRel()

    def __str__(self):
        return str(self.teacher_id) + ' ' + self.f_name
