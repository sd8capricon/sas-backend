from django.urls import path
from api import views

urlpatterns = [
    path('login/', views.login),
    path('verify/', views.verifyToken),
    path('students/', views.students_details),
    path('cal-students-atten/', views.cal_total_attendance_percentage),
    path('teachers/', views.teachers_details),
    path('teacher/<int:teacher_id>/', views.teacher),
    path('courses/', views.courses_detail),
    path('course/<int:course_id>/', views.course),
    path('course-lec-stats/<int:course_id>/', views.course_lec_stats),
    path('all-course-stats/', views.all_course_stats),
    path('attendance/<int:courseId>/<int:lec_no>/', views.attendance),
    path('get-last-lec/<int:course_id>/', views.get_last_lecnum),
    path('defaulters/', views.getDefaulters),
    path('email-defaultors/', views.email_defaultors)
]