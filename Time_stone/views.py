
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import *





@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

def login_page(request):
    return render(request, 'login.html')


def form(request):
    if request.method == 'POST':
        Name = request.POST.get('name')
        Email = request.POST.get('email')
        Age = int(request.POST.get('age'))

        Student.objects.create(name=Name, age=Age, email=Email)

        return redirect('student_list')

    return render(request, 'form.html')


def new(request):
    Students = Student.objects.all()
    return render(request, 'new.html', {'Students': Students})


def student_list(request):
    Students = Student.objects.all()
    return render(request, 'new.html', {'Students': Students})


def student_update(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.email = request.POST.get('email')
        student.age = int(request.POST.get('age'))

        student.save()

        return redirect('student_list')

    return render(request, 'std_update.html', {'student': student})


def student_delete(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.delete()

    return redirect('student_list')




# user authentication

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})




def user_login(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'login.html')



def user_logout(request):
    logout(request)
    return redirect('login')