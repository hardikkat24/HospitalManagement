from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Prescription, Appointment, Invoice, Contact

# only for signup form
POSITION_CHOICES = [
    ('P', 'Patient'),
    ('D', 'Doctor'),
]

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput()
    )

    email = forms.EmailField(
        label="Email ",
        widget=forms.EmailInput()
    )
        
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput()
    )

    password2 = forms.CharField(
        label="Re-enter your password",
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# while registration
class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput()
    ) 

    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput()
    ) 

    position = forms.ChoiceField(
        choices = POSITION_CHOICES,
        label="Select one",
        widget=forms.Select()
    ) 

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'position')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'position','status', 'department', 'attendance', 'salary')


class DoctorProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'position','status', 'department', 'attendance', 'salary', 'med_rep', 'case_paper')


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model =Prescription
        exclude = ('date', 'doctor')


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'patient', 'date', 'time', 'status']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone', 'gender', 'age', 'address', 'blood_group', 'med_rep', 'case_paper']


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone', 'gender', 'age', 'address', 'blood_group', 'status', 'department', 'attendance', 'salary']


class DoctorUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'position', 'med_rep', 'case_paper', )

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('patient', 'total', 'paid', 'invoice')

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ('date',)