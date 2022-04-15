from django.urls import path
from student import views

urlpatterns = [
    path('all/', views.index),
    path('<int:roll_no>/', views.read),
    path('enroll/', views.enroll),
    path('update/<int:roll_no>/', views.update),
    path('remove/<int:roll_no>/', views.remove)
]
