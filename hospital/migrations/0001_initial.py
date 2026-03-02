from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(default='Bangladesh', max_length=100)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('website', models.URLField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_profile', to='core.user')),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization', models.CharField(max_length=100)),
                ('qualification', models.CharField(max_length=200)),
                ('experience_years', models.PositiveIntegerField(default=0)),
                ('consultation_fee', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('available_days', models.CharField(default='Monday,Tuesday,Wednesday,Thursday,Friday', max_length=200)),
                ('bio', models.TextField(blank=True)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('address', models.TextField(blank=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_profile', to='core.user')),
                ('hospital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctors', to='hospital.hospital')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.department')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover_letter', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')], default='PENDING', max_length=20)),
                ('response_message', models.TextField(blank=True)),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('reviewed_at', models.DateTimeField(blank=True, null=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='hospital.doctor')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='hospital.hospital')),
            ],
            options={'ordering': ['-applied_at'], 'unique_together': {('doctor', 'hospital')}},
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('blood_group', models.CharField(blank=True, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=5)),
                ('address', models.TextField(blank=True)),
                ('emergency_contact', models.CharField(blank=True, max_length=15)),
                ('medical_history', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient_profile', to='core.user')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateField()),
                ('appointment_time', models.TimeField()),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('CONFIRMED', 'Confirmed'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')], default='PENDING', max_length=20)),
                ('symptoms', models.TextField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='hospital.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='hospital.patient')),
            ],
            options={'ordering': ['-appointment_date', '-appointment_time']},
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosis', models.TextField()),
                ('prescription', models.TextField(blank=True)),
                ('follow_up_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('appointment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='medical_record', to='hospital.appointment')),
            ],
        ),
    ]
