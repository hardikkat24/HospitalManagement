from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

POSITION_CHOICES = [
    ('P', 'Patient'),
    ('D', 'Doctor'),
    ('H', 'HR'),
    ('R', 'Receptionist')
]

GENDER_CHOICES = [
    ('M', 'Male'), 
    ('F', 'Female'), 
    ('O', 'Other'), 
]

BLOOD_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    position = models.CharField(max_length = 25, choices = POSITION_CHOICES, default = "P")

    # next records seen in update form 
    phone = models.CharField(max_length = 12, null = True, blank = True)
    gender = models.CharField(max_length = 1, choices = GENDER_CHOICES, null = True, blank = True)
    age = models.IntegerField(null = True, blank = True)
    address = models.TextField(null = True, blank = True)
    blood_group = models.CharField(max_length = 3, choices = BLOOD_CHOICES, null = True, blank = True)

    # only for patients
    med_rep = models.FileField(null = True, blank = True)
    case_paper = models.IntegerField(null = True, blank = True)

    # only for docs
    status = models.BooleanField(null = True, blank = True)
    department = models.CharField(max_length = 100, null = True, blank = True)
    attendance = models.IntegerField(null = True, blank = True)
    salary = models.IntegerField(null = True, blank = True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    @property
    def outstanding(self):
        invoices = self.user.patient_inv.all()
        outstanding = 0
        for invoice in invoices:
            outstanding += invoice.outstanding

        return outstanding

    @property
    def paid(self):
        invoices = self.user.patient_inv.all()
        paid = 0
        for invoice in invoices:
            paid += invoice.paid

        return paid


class Appointment(models.Model):
    doctor = models.ForeignKey(User, on_delete = models.SET_NULL, related_name = "doctor_app", null = True)
    patient = models.ForeignKey(User, on_delete = models.SET_NULL, related_name = "patient_app", null = True)
    date = models.DateField()
    time = models.TimeField()
    status = models.BooleanField(default = False)

    def __str__(self):
        return self.patient.profile.full_name + " with " + self.doctor.profile.full_name


class Prescription(models.Model):
    doctor = models.ForeignKey(User, on_delete = models.SET_NULL, related_name = "doctor_pres", null = True)
    patient = models.ForeignKey(User, on_delete = models.SET_NULL, related_name = "patient_pres", null = True)
    prescription = models.TextField()
    disease = models.TextField()
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.doctor.profile.full_name + " to " + self.patient.profile.full_name


class Invoice(models.Model):
    patient = models.ForeignKey(User, on_delete = models.SET_NULL, related_name = "patient_inv", null = True)
    total = models.IntegerField()
    paid = models.IntegerField()
    date = models.DateTimeField(auto_now_add = True)
    invoice = models.FileField(null = True, blank = True, upload_to = 'invoice/')

    def __str__(self):
        return self.patient.username + "'s " + str(self.total)

    @property
    def outstanding(self):
        return self.total - self.paid

    @property
    def invoiceURL(self):
        try:
            url = self.invoice.url
        except:
            url = ''
        
        return url


class Contact(models.Model):
    full_name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 256)
    phone = models.CharField(blank = True, null = True, max_length= 12)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.full_name
