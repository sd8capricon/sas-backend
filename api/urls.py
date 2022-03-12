from django.urls import path
from api import views

urlpatterns = [
    path('login/', views.login),
    path('verify/', views.verifyToken),
    path('students/', views.students_details),
    path('student/<int:roll_no>/', views.student),
    path('teachers/', views.teachers_details),
    path('teacher/<int:teacher_id>/', views.teacher),
    path('courses/', views.courses_detail),
    path('course/<int:course_id>/', views.course),
    path('course-lec-stats/<int:course_id>/', views.course_attendance_percentage),
    path('attendance/<int:courseId>/<int:lec_no>/', views.attendance),
]