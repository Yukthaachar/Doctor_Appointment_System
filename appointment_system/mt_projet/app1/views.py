from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, PatientRegisterForm, DoctorRegisterForm, LoginForm, AppointmentForm,DoctorProfileForm, PatientProfileForm
from .models import Doctor, Patient, Appointment
from datetime import datetime,date,time
def index(request):
    return render(request, 'index.html')

def login_view(request, role):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if role == 'patient':
                    return redirect('patient_dashboard')
                elif role == 'doctor':
                    return redirect('doctor_dashboard')
                else:
                    return redirect('admin_dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'role': role})

def register_view(request, role):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if role == 'patient':
            profile_form = PatientRegisterForm(request.POST)
        elif role == 'doctor':
            profile_form = DoctorRegisterForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login_view', role=role)
    else:
        user_form = UserRegisterForm()
        if role == 'patient':
            profile_form = PatientRegisterForm()
        elif role == 'doctor':
            profile_form = DoctorRegisterForm()

    if role == 'patient':
        return render(request, 'register_patient.html', {'user_form': user_form, 'profile_form': profile_form, 'role': role})
    elif role == 'doctor':
        return render(request, 'register_doctor.html', {'user_form': user_form, 'profile_form': profile_form, 'role': role})


@login_required
def patient_dashboard(request):
    patient = Patient.objects.get(user=request.user)
    appointments = Appointment.objects.filter(patient=patient)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()
            return redirect('patient_dashboard')  # Redirect after successfully saving appointment
    else:
        form = AppointmentForm()
    
    return render(request, 'patient_dashboard.html', {'appointments': appointments, 'form': form})


@login_required
def doctor_dashboard(request):
    appointments = Appointment.objects.filter(doctor=request.user.doctor)

    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        status = request.POST.get('status')

        appointment = get_object_or_404(Appointment, pk=appointment_id)
        
        if status == 'Accepted':
            appointment.status = 'Accepted'
            appointment.is_accepted = True  # Update the new field
            appointment.save()
            messages.success(request, f'Appointment with {appointment.patient.user.username} accepted.')

            # Notify patient (example: you can send an email here or use other notification methods)
            # For simplicity, let's assume you're just updating the appointment status for the patient view.

        elif status == 'Rejected':
            appointment.status = 'Rejected'
            appointment.is_accepted = False  # Update the new field
            appointment.save()
            messages.info(request, f'Appointment with {appointment.patient.user.username} rejected.')

            # Notify patient (example: send an email or update status in patient view)

        return redirect('doctor_dashboard')

    return render(request, 'doctor_dashboard.html', {'appointments': appointments})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def patient_profile(request):
    patient = Patient.objects.get(user=request.user)
    return render(request, 'patient_profile.html', {'patient': patient})

def doctor_profile(request):
    doctor = Doctor.objects.get(user=request.user)
    context = {
        'doctor': doctor,
    }
    return render(request, 'doctor_profile.html', context)


@login_required
def book_appointment(request):
    doctors = Doctor.objects.all()
    error_message = None
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            doctor = form.cleaned_data['doctor']
            appointment_date = form.cleaned_data['appointment_date']
            appointment_time = form.cleaned_data['appointment_time']
            
            # Check if the appointment slot is already booked
            if Appointment.objects.filter(
                doctor=doctor, 
                appointment_date=appointment_date, 
                appointment_time=appointment_time
            ).exists():
                return render(request, 'appointment_error.html', {
                    'error_message': 'This appointment slot is already booked. Please choose a different time.'
                })
            
            # Check if appointment date is in the past
            if appointment_date < date.today():
                return render(request, 'appointment_error.html', {
                    'error_message': 'Appointment date cannot be in the past.'
                })
            
            # Check if appointment time is in the past for today's date
            current_time = datetime.now().time()
            if appointment_date == date.today() and appointment_time < current_time:
                return render(request, 'appointment_error.html', {
                    'error_message': 'Appointment time cannot be in the past.'
                })
            
            # Ensure patient object is created for the user
            patient, created = Patient.objects.get_or_create(user=request.user)
            
            # Save the appointment with the patient info
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()
            
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()
    
    # Render the form without error message (if no error occurs)
    return render(request, 'book_appointment.html', {
        'form': form,
        'doctors': doctors,
    })

@login_required
def edit_doctor_profile(request):
    doctor = Doctor.objects.get(user=request.user)  # Assuming Doctor is related to User
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_profile')
    else:
        form = DoctorProfileForm(instance=doctor)
    
    return render(request, 'edit_doctor_profile.html', {'form': form, 'doctor': doctor})

@login_required
def edit_patient_profile(request):
    patient = Patient.objects.get(user=request.user)  # Assuming Doctor is related to User
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_profile')
    else:
        form = PatientProfileForm(instance=patient)
    
    return render(request, 'edit_patient_profile.html', {'form': form, 'patient': patient})

def doctors_by_specialization(request):
    specializations = Doctor.objects.values_list('specialization', flat=True).distinct()
    selected_specialization = request.GET.get('specialization')
    doctors = Doctor.objects.filter(specialization=selected_specialization) if selected_specialization else None
    
    return render(request, 'doctors_by_specialization.html', {
        'specializations': specializations,
        'selected_specialization': selected_specialization,
        'doctors': doctors,
    })