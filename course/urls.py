from django.urls import path
from course import views


urlpatterns = [
    path('', views.index),
    path('update/<int:course_id>', views.update),
]
