from django.contrib import admin
from api.models import Student, Teacher, Course, Attendance, Lec_Stat

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Attendance)
admin.site.register(Lec_Stat)