from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),

    path('admin-dashboard/',
         views.admin_dashboard,
         name='admin_dashboard'),

    path('add-doctor/',
         views.add_doctor,
         name='add_doctor'),

    path('doctor-dashboard/',
         views.doctor_dashboard,
         name='doctor_dashboard'),

    path('update-status/<int:appointment_id>/',
         views.update_status,
         name='update_status'),

    path('patient-dashboard/',
         views.patient_dashboard,
         name='patient_dashboard'),

    path('book-appointment/',
         views.book_appointment,
         name='book_appointment'),

    path('cancel-appointment/<int:appointment_id>/',
         views.cancel_appointment,
         name='cancel_appointment'),
]
