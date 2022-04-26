from django.urls import path
from faculty import views


urlpatterns = [
    path('all/', views.index),
    path('register/', views.register),
    path('update/<int:user_id>', views.update),
    path('remove/<int:id>/', views.remove)
]
