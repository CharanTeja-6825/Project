from django.urls import path
from . import views

app_name = 'trainer'

urlpatterns = [
    path('homepage_trainer/', views.homepage_trainer, name='homepage_trainer'),
    path('my-courses/', views.assigned_courses, name='my_courses'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('assigned_employees/', views.trainer_assigned_employees, name='assigned_employees'),
    path('trainer/<int:trainer_id>/', views.trainer_courses, name='trainer_courses'),
]