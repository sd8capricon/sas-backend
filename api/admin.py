from django.contrib import admin
from api.models import Student, Teacher, Course, Attendance

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Attendance)