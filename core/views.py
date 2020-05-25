from django.shortcuts import render, redirect
from .forms import SignUpForm, ProfileForm, ProfileUpdateForm, PrescriptionForm, AppointmentForm, PatientForm, DoctorForm, DoctorUpdateForm, DoctorProfileUpdateForm, InvoiceForm, ContactForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Appointment, Prescription, Profile, Invoice


def register(request):
    if request.method == "POST":
        form1 = SignUpForm(request.POST)
        form2 = ProfileForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            profile = form2.save(commit = False)
            profile.user = user
            profile.save()
            messages.success(request, "Successfully Registered!")
            return redirect('login')
    else:
        form1 = SignUpForm()
        form2 = ProfileForm()

    context = {
        'form1': form1,
        'form2': form2
    }

    return render(request, "core/signup.html", context)


def home(request):
    return render(request, "core/home.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message sent successfully!")
    else:
        form = ContactForm()

    context = {
        'form': form
    }

    return render(request, "core/contact.html", context)


def about_us(request):
    return render(request, "core/about_us.html")

# patients
@login_required
def update_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance = request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
    
    else:
        form = ProfileUpdateForm(instance = request.user.profile)

    context = {
        'form': form,
    }

    return render(request, "core/update_profile.html", context)


@login_required
def patient_appointments(request):
    appointments = Appointment.objects.filter( patient__exact = request.user )
    context = {
        'appointments': appointments
    }

    return render(request, "core/patient_appointments.html", context)

@login_required
def patient_invoice(request):
    invoices = request.user.patient_inv.all()
    context = {
        'invoices': invoices,
    }

    return render(request, "core/patient_invoice.html", context)


@login_required
def patient_prescriptions(request):
    prescriptions = Prescription.objects.filter( patient__exact = request.user ).order_by('-date')
    context = {
        'prescriptions': prescriptions
    }

    return render(request, "core/patient_prescriptions.html", context)




# doctors
@login_required
def doctor_update_profile(request):
    if request.method == "POST":
        form = DoctorProfileUpdateForm(request.POST, instance = request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
    
    else:
        form = DoctorProfileUpdateForm(instance = request.user.profile)

    context = {
        'form': form,
    }

    return render(request, "core/doctor_update_profile.html", context)


@login_required
def doctor_appointments(request):
    appointments = Appointment.objects.filter( doctor__exact = request.user )
    context = {
        'appointments': appointments
    }

    return render(request, "core/doctor_appointments.html", context)

@login_required
def doctor_prescriptions(request):
    prescriptions = Prescription.objects.filter( doctor__exact = request.user ).order_by('-date')
    context = {
        'prescriptions': prescriptions
    }

    return render(request, "core/doctor_prescriptions.html", context)

@login_required
def doctor_create_prescription(request):
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            pres = form.save(commit = False)
            pres.doctor = request.user
            pres.save()
            messages.success(request, "Prescription created successfully!")
            return redirect('doctor-prescriptions')
    else:
        form = PrescriptionForm()
    context = {
        'form': form
    }

    return render(request, "core/doctor_create_prescription.html", context)




# Receptionist
@login_required
def receptionist_dashboard(request):
    appointments = Appointment.objects.all().order_by('-date')
    patients = Profile.objects.filter( position__exact = 'P' )
    total_appointments = Appointment.objects.count()
    appointments_done = Appointment.objects.filter(status__exact = True).count()
    upcoming_appointments = total_appointments - appointments_done

    context = {
        'appointments': appointments,
        'patients': patients,
        'total_appointments': total_appointments,
        'appointments_done': appointments_done,
        'upcoming_appointments': upcoming_appointments,
    }

    return render(request, "core/receptionist_dashboard.html", context)


@login_required
def receptionist_create_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment created successfully!")
            return redirect('receptionist-dashboard')
    else:
        form = AppointmentForm()

    context = {
        'form': form,
    }

    return render(request, "core/receptionist_create_appointment.html", context)


@login_required
def receptionist_complete_appointment(request, pk):
    appointment = Appointment.objects.get(pk = pk)
    appointment.status = True
    appointment.save()
    messages.success(request, "Appointment marked as completed!")
    return redirect('receptionist-dashboard')


@login_required
def receptionist_create_patient(request):
    if request.method == "POST":
        form1 = SignUpForm(request.POST)
        form2 = PatientForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            patient = form2.save(commit = False)
            patient.user = user
            patient.position = 'P'
            patient.save()
            messages.success(request, "Patient created successfully!")
            return redirect('receptionist-dashboard')
    else:
        form1 = SignUpForm()
        form2 = PatientForm()

    context = {
        'form1': form1,
        'form2': form2
    }

    return render(request, "core/receptionist_create_patient.html", context)


@login_required
def receptionist_update_patient(request, pk):
    patient = Profile.objects.get(pk = pk)
    if request.method == "POST":
        form2 = PatientForm(request.POST, instance = patient)
        if form2.is_valid():
            form2.save()
            messages.success(request, "Patient updated successfully!")
            return redirect('receptionist-dashboard')
    else:
        form2 = PatientForm(instance = patient)

    context = {
        'form2': form2
    }

    return render(request, "core/receptionist_update_patient.html", context)


@login_required
def receptionist_delete_patient(request, pk):
    patient = Profile.objects.get(pk = pk)
    if request.method == "POST":
        patient.user.delete()
        patient.delete()
        messages.success(request, "Patient deleted successfully!")
        return redirect('receptionist-dashboard')
    

    context = {
        'patient': patient
    }

    return render(request, "core/receptionist_delete_patient.html", context)


@login_required
def receptionist_manage_invoice(request):
    invoices = Invoice.objects.all().order_by('-date')

    context = {
        'invoices': invoices
    }

    return render(request, "core/receptionist_manage_invoice.html", context)


@login_required
def receptionist_create_invoice(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Invoice created successfully!")
            return redirect('receptionist-manage-invoice')
    else:
        form = InvoiceForm()

    context = {
        'form': form,
    }

    return render(request, "core/receptionist_create_invoice.html", context)




#HR
@login_required
def hr_dashboard(request):
    doctors = Profile.objects.filter( position__exact = "D" )
    total_doctors = doctors.count()
    total_patients = Profile.objects.filter( position__exact = "P" ).count()
    on_duty_doctors = doctors.filter( status__exact = True ).count()

    context = {
        'doctors': doctors,
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'on_duty_doctors': on_duty_doctors,
    }

    return render(request, "core/hr_dashboard.html", context)


@login_required
def hr_create_doctor(request):
    if request.method == "POST":
        form1 = SignUpForm(request.POST)
        form2 = DoctorForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            patient = form2.save(commit = False)
            patient.user = user
            patient.position = 'D'
            patient.save()
            messages.success(request, "Doctor created successfully!")
            return redirect('hr-dashboard')
    else:
        form1 = SignUpForm()
        form2 = DoctorForm()

    context = {
        'form1': form1,
        'form2': form2
    }

    return render(request, "core/hr_create_doctor.html", context)


@login_required
def hr_update_doctor(request, pk):
    doctor = Profile.objects.get(pk = pk)
    if request.method == "POST":
        form2 = DoctorUpdateForm(request.POST, instance = doctor)
        if form2.is_valid():
            form2.save()
            messages.success(request, "Patient updated successfully!")
            return redirect('hr-dashboard')
    else:
        form2 = DoctorUpdateForm(instance = doctor)

    context = {
        'form2': form2
    }

    return render(request, "core/hr_update_doctor.html", context)


@login_required
def hr_delete_doctor(request, pk):
    doctor = Profile.objects.get(pk = pk)
    if request.method == "POST":
        doctor.user.delete()
        doctor.delete()
        messages.success(request, "Doctor deleted successfully!")
        return redirect('hr-dashboard')
    

    context = {
        'doctor': doctor,
    }

    return render(request, "core/hr_delete_doctor.html", context)


@login_required
def hr_accounting(request):
    patients = Profile.objects.filter( position__exact = 'P' )
    invoices = Invoice.objects.all().order_by('-date')

    context = {
        'patients': patients,
        'invoices': invoices,
    }

    return render(request, "core/hr_accounting.html", context)


@login_required
def hr_patient_contact(request, pk):
    patient = Profile.objects.get(pk = pk)

    context = {
        'patient': patient
    }

    return render(request, "core/hr_patient_contact.html", context)