from django.urls import path
from api import views

urlpatterns = [
    path('student/', views.student_details),
    path('teacher/', views.teacher_details),
    path('create-course/', views.course),
    path('attendance/<int:course_id>/', views.attendance),
]