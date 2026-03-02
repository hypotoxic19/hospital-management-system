from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .models import Doctor, Patient, Appointment, MedicalRecord, Department, Hospital, DoctorApplication
from .forms import (
    DoctorProfileForm, PatientProfileForm, AppointmentForm,
    MedicalRecordForm, AppointmentStatusForm, HospitalProfileForm,
    DoctorApplicationForm, ApplicationReviewForm
)

@csrf_exempt
# ─── Hospital Profile ───────────────────────────────────────────
@login_required
def hospital_profile(request):
    if request.user.role != 'HOSPITAL':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    try:
        hospital = Hospital.objects.get(user=request.user)
    except Hospital.DoesNotExist:
        hospital = None

    if request.method == 'POST':
        form = HospitalProfileForm(request.POST, instance=hospital)
        if form.is_valid():
            h = form.save(commit=False)
            h.user = request.user
            h.save()
            messages.success(request, 'Hospital profile saved!')
            return redirect('hospital_profile')
    else:
        form = HospitalProfileForm(instance=hospital)
    return render(request, 'hospital/hospital_profile.html', {'form': form, 'hospital': hospital})



# ─── Applications (Hospital side) ──────────────────────────────
@login_required
def application_list(request):
    if request.user.role != 'HOSPITAL':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    try:
        hospital = Hospital.objects.get(user=request.user)
    except Hospital.DoesNotExist:
        messages.warning(request, 'Please complete your hospital profile first.')
        return redirect('hospital_profile')

    status_filter = request.GET.get('status', '')
    applications = DoctorApplication.objects.filter(hospital=hospital).select_related('doctor__user', 'doctor__department')
    if status_filter:
        applications = applications.filter(status=status_filter)

    return render(request, 'hospital/application_list.html', {
        'applications': applications,
        'hospital': hospital,
        'status_filter': status_filter,
    })


@login_required
def application_review(request, pk):
    if request.user.role != 'HOSPITAL':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    try:
        hospital = Hospital.objects.get(user=request.user)
    except Hospital.DoesNotExist:
        return redirect('hospital_profile')

    application = get_object_or_404(DoctorApplication, pk=pk, hospital=hospital)

    if request.method == 'POST':
        form = ApplicationReviewForm(request.POST, instance=application)
        if form.is_valid():
            app = form.save(commit=False)
            app.reviewed_at = timezone.now()
            app.save()
            # If accepted, link doctor to this hospital
            if app.status == 'ACCEPTED':
                app.doctor.hospital = hospital
                app.doctor.save()
            elif app.status == 'REJECTED':
                # Remove from hospital if previously accepted
                if app.doctor.hospital == hospital:
                    app.doctor.hospital = None
                    app.doctor.save()
            messages.success(request, f'Application {app.status.lower()} successfully.')
            return redirect('application_list')
    else:
        form = ApplicationReviewForm(instance=application)

    return render(request, 'hospital/application_review.html', {
        'application': application,
        'form': form,
    })


# ─── Applications (Doctor side) ────────────────────────────────
@login_required
def doctor_apply(request):
    if request.user.role != 'DOCTOR':
        messages.error(request, 'Only doctors can apply to hospitals.')
        return redirect('dashboard')
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        messages.warning(request, 'Please complete your doctor profile first.')
        return redirect('doctor_profile')

    existing_applications = DoctorApplication.objects.filter(doctor=doctor).select_related('hospital')

    if request.method == 'POST':
        form = DoctorApplicationForm(request.POST)
        if form.is_valid():
            hospital = form.cleaned_data['hospital']
            if DoctorApplication.objects.filter(doctor=doctor, hospital=hospital).exists():
                messages.warning(request, f'You have already applied to {hospital.name}.')
            else:
                app = form.save(commit=False)
                app.doctor = doctor
                app.save()
                messages.success(request, f'Application sent to {hospital.name}!')
                return redirect('doctor_apply')
    else:
        form = DoctorApplicationForm()

    return render(request, 'hospital/doctor_apply.html', {
        'form': form,
        'applications': existing_applications,
        'doctor': doctor,
    })


# ─── Doctors ────────────────────────────────────────────────────
def doctor_list(request):
    query = request.GET.get('q', '')
    dept = request.GET.get('dept', '')
    city = request.GET.get('city', '')
    # Only show doctors that are accepted (linked to a hospital)
    doctors = Doctor.objects.filter(is_available=True, hospital__isnull=False).select_related('user', 'department', 'hospital')
    if query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(specialization__icontains=query)
        )
    if dept:
        doctors = doctors.filter(department_id=dept)
    if city:
        doctors = doctors.filter(city__icontains=city)
    departments = Department.objects.all()
    cities = Doctor.objects.filter(hospital__isnull=False).exclude(city='').values_list('city', flat=True).distinct()
    return render(request, 'hospital/doctor_list.html', {
        'doctors': doctors, 'departments': departments,
        'query': query, 'selected_dept': dept, 'cities': cities, 'selected_city': city,
    })


def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'hospital/doctor_detail.html', {'doctor': doctor})


@login_required
def doctor_profile(request):
    if request.user.role != 'DOCTOR':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        doctor = None

    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=doctor)
        if form.is_valid():
            d = form.save(commit=False)
            d.user = request.user
            d.save()
            messages.success(request, 'Profile saved!')
            return redirect('doctor_profile')
    else:
        form = DoctorProfileForm(instance=doctor)
    return render(request, 'hospital/doctor_profile.html', {'form': form, 'doctor': doctor})


# ─── Patients ───────────────────────────────────────────────────
@login_required
def patient_profile(request):
    if request.user.role != 'PATIENT':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        patient = None

    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient)
        if form.is_valid():
            p = form.save(commit=False)
            p.user = request.user
            p.save()
            messages.success(request, 'Profile saved!')
            return redirect('patient_profile')
    else:
        form = PatientProfileForm(instance=patient)
    return render(request, 'hospital/patient_profile.html', {'form': form, 'patient': patient})


# ─── Appointments ───────────────────────────────────────────────
@login_required
def book_appointment(request):
    if request.user.role != 'PATIENT':
        messages.error(request, 'Only patients can book appointments.')
        return redirect('dashboard')
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        messages.warning(request, 'Please complete your patient profile first.')
        return redirect('patient_profile')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save(commit=False)
            appt.patient = patient
            appt.save()
            messages.success(request, 'Appointment booked!')
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'hospital/book_appointment.html', {'form': form})


@login_required
def appointment_list(request):
    user = request.user
    if user.role == 'PATIENT':
        try:
            patient = Patient.objects.get(user=user)
            appointments = Appointment.objects.filter(patient=patient)
        except Patient.DoesNotExist:
            appointments = Appointment.objects.none()
    elif user.role == 'DOCTOR':
        try:
            doctor = Doctor.objects.get(user=user)
            appointments = Appointment.objects.filter(doctor=doctor)
        except Doctor.DoesNotExist:
            appointments = Appointment.objects.none()
    else:
        appointments = Appointment.objects.all()
    return render(request, 'hospital/appointment_list.html', {'appointments': appointments})


@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    user = request.user
    is_patient = user.role == 'PATIENT' and hasattr(user, 'patient_profile') and appointment.patient == user.patient_profile
    is_doctor = user.role == 'DOCTOR' and hasattr(user, 'doctor_profile') and appointment.doctor == user.doctor_profile
    is_admin = user.role == 'HOSPITAL' or user.is_superuser
    if not (is_patient or is_doctor or is_admin):
        messages.error(request, 'Access denied.')
        return redirect('appointment_list')

    medical_record = None
    try:
        medical_record = appointment.medical_record
    except MedicalRecord.DoesNotExist:
        pass

    status_form = record_form = None
    if is_doctor or is_admin:
        if request.method == 'POST':
            if 'update_status' in request.POST:
                status_form = AppointmentStatusForm(request.POST, instance=appointment)
                if status_form.is_valid():
                    status_form.save()
                    messages.success(request, 'Appointment updated.')
                    return redirect('appointment_detail', pk=pk)
            elif 'add_record' in request.POST:
                record_form = MedicalRecordForm(request.POST, instance=medical_record)
                if record_form.is_valid():
                    rec = record_form.save(commit=False)
                    rec.appointment = appointment
                    rec.save()
                    messages.success(request, 'Medical record saved.')
                    return redirect('appointment_detail', pk=pk)
        else:
            status_form = AppointmentStatusForm(instance=appointment)
            record_form = MedicalRecordForm(instance=medical_record)

    return render(request, 'hospital/appointment_detail.html', {
        'appointment': appointment,
        'medical_record': medical_record,
        'status_form': status_form,
        'record_form': record_form,
        'is_doctor': is_doctor,
        'is_admin': is_admin,
    })


@login_required
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    user = request.user
    is_owner = (user.role == 'PATIENT' and hasattr(user, 'patient_profile') and appointment.patient == user.patient_profile)
    if not (is_owner or user.role == 'HOSPITAL' or user.is_superuser):
        messages.error(request, 'Access denied.')
        return redirect('appointment_list')
    appointment.status = 'CANCELLED'
    appointment.save()
    messages.success(request, 'Appointment cancelled.')
    return redirect('appointment_list')


from django.contrib.auth.decorators import login_required

@login_required
def my_applications(request):
    # Add your logic here later
    return render(request, 'hospital/my_applications.html', {})