from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import Doctor, Patient, Appointment







# ROLE CHECKING

def is_admin(user):
    return user.is_authenticated and user.is_staff


def is_doctor(user):
    return user.is_authenticated and hasattr(user, 'doctor')


def is_patient(user):
    return user.is_authenticated and hasattr(user, 'patient')


# HOME

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        if hasattr(request.user, 'doctor'):
            return redirect('doctor_dashboard')
        if hasattr(request.user, 'patient'):
            return redirect('patient_dashboard')

    return redirect('login')


# PATIENT REGISTRATION

def register(request):

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()

        if not all([username, email, password, age,
                    gender, phone, address]):
            messages.error(request, 'Please fill all fields.')
            return redirect('register')

        if len(password) < 8:
            messages.error(request, 'Password must have at least 8 characters.')
            return redirect('register')

        try:
            age = int(age)
            if age < 1 or age > 120:
                raise ValueError
        except ValueError:
            messages.error(request, 'Enter a valid age.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Patient.objects.create(
            user=user,
            age=age,
            gender=gender,
            phone=phone,
            address=address
        )

        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')

    return render(request, 'register.html')


# LOGIN

def user_login(request):

    if request.user.is_authenticated:
        return home(request)

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')

            elif hasattr(user, 'doctor'):
                login(request, user)
                return redirect('doctor_dashboard')

            elif hasattr(user, 'patient'):
                login(request, user)
                return redirect('patient_dashboard')

            messages.error(request, 'User role not configured.')

        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


# LOGOUT

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


# ADMIN DASHBOARD

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):

    doctors = Doctor.objects.select_related('user').all()
    patients = Patient.objects.select_related('user').all()

    appointments = Appointment.objects.select_related(
        'patient__user',
        'doctor__user'
    ).order_by('-created_at')

    context = {
        'doctors': doctors,
        'patients': patients,
        'appointments': appointments,
        'doctor_count': doctors.count(),
        'patient_count': patients.count(),
        'appointment_count': appointments.count(),
    }

    return render(
        request,
        'admin_dashboard.html',
        context
    )


# ADD DOCTOR

@login_required
@user_passes_test(is_admin)
def add_doctor(request):

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        specialization = request.POST.get('specialization', '').strip()
        phone = request.POST.get('phone', '').strip()

        if not all([username, email, password,
                    specialization, phone]):
            messages.error(request, 'Please fill all fields.')
            return redirect('add_doctor')

        if len(password) < 8:
            messages.error(request, 'Password must have at least 8 characters.')
            return redirect('add_doctor')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('add_doctor')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('add_doctor')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Doctor.objects.create(
            user=user,
            specialization=specialization,
            phone=phone
        )

        messages.success(request, 'Doctor added successfully!')
        return redirect('admin_dashboard')

    return render(request, 'add_doctor.html')


# DOCTOR DASHBOARD

@login_required
@user_passes_test(is_doctor)
def doctor_dashboard(request):

    doctor = get_object_or_404(
        Doctor,
        user=request.user
    )

    appointments = Appointment.objects.filter(
        doctor=doctor
    ).select_related(
        'patient__user'
    ).order_by('-appointment_date')

    return render(
        request,
        'doctor_dashboard.html',
        {'appointments': appointments}
    )


# UPDATE APPOINTMENT STATUS

@login_required
@user_passes_test(is_doctor)
@require_POST
def update_status(request, appointment_id):

    doctor = get_object_or_404(
        Doctor,
        user=request.user
    )

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=doctor
    )

    status = request.POST.get('status')

    allowed_statuses = [
        'Approved',
        'Rejected',
        'Completed'
    ]

    if status not in allowed_statuses:
        messages.error(request, 'Invalid status.')
        return redirect('doctor_dashboard')

    if appointment.status != 'Pending':
        messages.error(request, 'Only pending appointments can be updated.')
        return redirect('doctor_dashboard')

    appointment.status = status
    appointment.save()

    messages.success(request, 'Appointment status updated.')

    return redirect('doctor_dashboard')


# PATIENT DASHBOARD

@login_required
@user_passes_test(is_patient)
def patient_dashboard(request):

    patient = get_object_or_404(
        Patient,
        user=request.user
    )

    doctors = Doctor.objects.select_related('user').all()

    appointments = Appointment.objects.filter(
        patient=patient
    ).select_related(
        'doctor__user'
    ).order_by('-created_at')

    return render(
        request,
        'patient_dashboard.html',
        {
            'doctors': doctors,
            'appointments': appointments
        }
    )


# BOOK APPOINTMENT

@login_required
@user_passes_test(is_patient)
def book_appointment(request):

    doctors = Doctor.objects.select_related('user').all()

    if request.method == 'POST':

        doctor_id = request.POST.get('doctor')
        date = request.POST.get('appointment_date')
        reason = request.POST.get('reason', '').strip()

        if not doctor_id or not date or not reason:
            messages.error(request, 'Please fill all fields.')
            return redirect('book_appointment')

        try:
            appointment_date = timezone.datetime.strptime(
                date, '%Y-%m-%d'
            ).date()
        except ValueError:
            messages.error(request, 'Invalid appointment date.')
            return redirect('book_appointment')

        if appointment_date < timezone.localdate():
            messages.error(request, 'Select today or a future date.')
            return redirect('book_appointment')

        doctor = get_object_or_404(
            Doctor,
            id=doctor_id
        )

        patient = get_object_or_404(
            Patient,
            user=request.user
        )

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            reason=reason
        )

        messages.success(request, 'Appointment booked successfully!')
        return redirect('patient_dashboard')

    return render(
        request,
        'book_appointment.html',
        {'doctors': doctors}
    )


# CANCEL PENDING APPOINTMENT

@login_required
@user_passes_test(is_patient)
@require_POST
def cancel_appointment(request, appointment_id):

    patient = get_object_or_404(
        Patient,
        user=request.user
    )

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=patient
    )

    if appointment.status == 'Pending':
        appointment.status = 'Cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled.')
    else:
        messages.error(
            request,
            'Only pending appointments can be cancelled.'
        )

    return redirect('patient_dashboard')