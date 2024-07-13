from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/<str:role>/', views.login_view, name='login_view'),
    path('register/<str:role>/', views.register_view, name='register_view'),
    path('logout/', views.logout_view, name='logout'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/profile/', views.doctor_profile, name='doctor_profile'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('patient/profile/', views.patient_profile, name='patient_profile'),
    path('doctor/edit_profile/', views.edit_doctor_profile, name='edit_doctor_profile'),
    path('patient/edit_profile/', views.edit_patient_profile, name='edit_patient_profile'),
    path('doctors_by_specialization/', views.doctors_by_specialization, name='doctors_by_specialization'),
    path('doctor/profile/<int:id>/', views.doctor_profile, name='doctor_profile'),
    path('reschedule_appointment/<int:appointment_id>/', views.reschedule_appointment, name='reschedule_appointment'),
]
