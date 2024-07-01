# forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Patient, Doctor, Appointment

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PatientRegisterForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['age', 'medical_history']

class DoctorRegisterForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialization', 'experience']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'appointment_time']

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialization', 'experience']

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['age', 'medical_history']