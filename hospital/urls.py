from django.urls import path
from . import views

urlpatterns = [
    # Hospital
    path('profile/', views.hospital_profile, name='hospital_profile'),
    path('applications/', views.application_list, name='application_list'),
    path('applications/<int:pk>/review/', views.application_review, name='application_review'),
    # Doctor
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('doctor/profile/', views.doctor_profile, name='doctor_profile'),
    path('doctor/apply/', views.doctor_apply, name='doctor_apply'),
    # Patient
    path('patient/profile/', views.patient_profile, name='patient_profile'),
    # Appointments
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/book/', views.book_appointment, name='book_appointment'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:pk>/cancel/', views.cancel_appointment, name='cancel_appointment'),
]
