from django.urls import path
from . import views


app_name = 'admin_app'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('log_out/', views.log_out, name='log_out'),
    path('profile/', views.profile_page, name='profile_page'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/password/', views.update_password, name='update_password'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/edit/<int:course_id>/', views.update_course_view, name='edit_course'),
    path('courses/delete/<int:course_id>/', views.delete_course_view, name='delete_course'),
    path('courses/create/', views.create_course_view, name='create_course'),]

