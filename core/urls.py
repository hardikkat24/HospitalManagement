from django.urls import path, include
from . import views 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name = "register"),
    path('', views.home, name = "home"),
    path('login/', auth_views.LoginView.as_view(template_name="core/login.html"), name = "login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="core/logout.html"), name = "logout"),
    path('contact/', views.contact, name = "contact"),
    path('about-us/', views.about_us, name = "about-us"),
]

#patient
urlpatterns += [
    path('patient/appointments/', views.patient_appointments, name = "patient-appointments"),
    path('patient/invoice/', views.patient_invoice, name = "patient-invoice"),
    path('patient/prescriptions/', views.patient_prescriptions, name = "patient-prescriptions"),
    path('update/', views.update_profile, name = "update-profile"),
]

#doctor
urlpatterns += [
    path('doctor/appointments/', views.doctor_appointments, name = "doctor-appointments"),
    path('doctor/prescriptions/', views.doctor_prescriptions, name = "doctor-prescriptions"),
    path('doctor/create-prescription/', views.doctor_create_prescription, name = "doctor-create-prescription"),
    path('doctor/update/', views.doctor_update_profile, name = "doctor-update-profile"),
]

#receptionist
urlpatterns += [
    path('receptionist/dashboard/', views.receptionist_dashboard, name = "receptionist-dashboard"),
    path('receptionist/create-appointment/', views.receptionist_create_appointment, name = "receptionist-create-appointment"),
    path('receptionist/complete-appointment/<str:pk>/', views.receptionist_complete_appointment, name = "receptionist-complete-appointment"),
    path('receptionist/create-patient/', views.receptionist_create_patient, name = "receptionist-create-patient"),
    path('receptionist/update-patient/<str:pk>/', views.receptionist_update_patient, name = "receptionist-update-patient"),
    path('receptionist/delete-patient/<str:pk>/', views.receptionist_delete_patient, name = "receptionist-delete-patient"),
    path('receptionist/manage-invoice/', views.receptionist_manage_invoice, name = "receptionist-manage-invoice"),
    path('receptionist/create-invoice/', views.receptionist_create_invoice, name = "receptionist-create-invoice"),
]

#HR
urlpatterns += [
    path('hr/dashboard/', views.hr_dashboard, name = "hr-dashboard"),
    path('hr/create-doctor/', views.hr_create_doctor, name = "hr-create-doctor"),
    path('hr/update-doctor/<str:pk>/', views.hr_update_doctor, name = "hr-update-doctor"),
    path('hr/delete-doctor/<str:pk>/', views.hr_delete_doctor, name = "hr-delete-doctor"),
    path('hr/accounting/', views.hr_accounting, name = "hr-accounting"),
    path('hr/patient-contact/<str:pk>/', views.hr_patient_contact, name = "hr-patient-contact"),
]