from django.urls import path
from api import views

urlpatterns = [
    path('student/', views.student_details),
    path('course/', views.course),
    path('attendance/', views.attendance),
]