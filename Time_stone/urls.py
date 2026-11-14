
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('form/', views.form, name='form'),
    path('new/', views.student_list, name='new'),
    path('student_list/', views.student_list, name='student_list'),
    path('update/<int:id>/', views.student_update, name='student_update'),
    path('delete/<int:id>/', views.student_delete, name='student_delete'),
]
