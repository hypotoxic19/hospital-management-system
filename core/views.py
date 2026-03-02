from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from hospital.models import Appointment, Doctor, Patient, Hospital, DoctorApplication


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            # Role-based redirect after signup
            if user.role == 'DOCTOR':
                messages.info(request, 'Please complete your doctor profile.')
                return redirect('doctor_profile')
            elif user.role == 'HOSPITAL':
                messages.info(request, 'Please complete your hospital profile.')
                return redirect('hospital_profile')
            else:
                messages.info(request, 'Please complete your patient profile.')
                return redirect('patient_profile')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    user = request.user
    context = {'user': user}

    if user.role == 'PATIENT':
        try:
            patient = Patient.objects.get(user=user)
            context['appointments'] = Appointment.objects.filter(patient=patient).order_by('-appointment_date')[:5]
            context['profile_complete'] = True
        except Patient.DoesNotExist:
            context['appointments'] = []
            context['profile_complete'] = False

    elif user.role == 'DOCTOR':
        try:
            doctor = Doctor.objects.get(user=user)
            context['appointments'] = Appointment.objects.filter(doctor=doctor).order_by('-appointment_date')[:5]
            context['doctor'] = doctor
            context['applications'] = DoctorApplication.objects.filter(doctor=doctor).order_by('-applied_at')[:5]
            context['profile_complete'] = True
        except Doctor.DoesNotExist:
            context['appointments'] = []
            context['applications'] = []
            context['profile_complete'] = False

    elif user.role == 'HOSPITAL':
        try:
            hospital = Hospital.objects.get(user=user)
            context['hospital'] = hospital
            context['total_doctors'] = Doctor.objects.filter(hospital=hospital).count()
            context['total_patients'] = Patient.objects.count()
            context['total_appointments'] = Appointment.objects.count()
            context['pending_applications'] = DoctorApplication.objects.filter(hospital=hospital, status='PENDING').count()
            context['recent_appointments'] = Appointment.objects.order_by('-appointment_date')[:8]
            context['profile_complete'] = True
        except Hospital.DoesNotExist:
            context['profile_complete'] = False

    return render(request, 'core/dashboard.html', context)
