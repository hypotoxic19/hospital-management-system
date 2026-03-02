from django import forms
from .models import Doctor, Patient, Appointment, MedicalRecord, Department, Hospital, DoctorApplication


class HospitalProfileForm(forms.ModelForm):
    class Meta:
        model = Hospital
        exclude = ['user', 'created_at']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        exclude = ['user', 'hospital', 'created_at']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['latitude'].widget.attrs['placeholder'] = 'e.g. 23.8103'
        self.fields['longitude'].widget.attrs['placeholder'] = 'e.g. 90.4125'


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['user', 'created_at']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'medical_history': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class DoctorApplicationForm(forms.ModelForm):
    class Meta:
        model = DoctorApplication
        fields = ['hospital', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell the hospital why you want to join...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['hospital'].queryset = Hospital.objects.all()
        self.fields['hospital'].label = 'Apply to Hospital'


class ApplicationReviewForm(forms.ModelForm):
    class Meta:
        model = DoctorApplication
        fields = ['status', 'response_message']
        widgets = {
            'response_message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional message to the doctor...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['status'].choices = [
            ('PENDING', 'Pending'),
            ('ACCEPTED', 'Accept'),
            ('REJECTED', 'Reject'),
        ]


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'appointment_time', 'symptoms']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
            'symptoms': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.filter(is_available=True, hospital__isnull=False)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        exclude = ['appointment', 'created_at']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'prescription': forms.Textarea(attrs={'rows': 3}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status', 'notes']
        widgets = {'notes': forms.Textarea(attrs={'rows': 2})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
