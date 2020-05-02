from django.contrib import admin
from django.urls import path
from . import views


app_name = 'marks_system'
urlpatterns = [
    path('', views.index),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user_creation/', views.user_creation, name='user_creation'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_students_marks/', views.add_students_marks, name='add_students_marks'),
    path('students_marklist/', views.students_marklist, name='students_marklist'),
    path('edit_marks/<int:pk>', views.edit_marks, name='update_marks'),
    path('delete_student/<int:pk>', views.delete_student, name='delete_student'),
    path('department_creation/', views.department_creation, name='department_creation')

]
