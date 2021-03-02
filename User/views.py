from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import CreateUserForm
from .decorators import *

def dashboard(request):
    context = {}
    return render(request, "User/dashboard.html", context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Akun {user} berhasil dibuat')
            redirect('login')
    
    context = {'form' : form}
    return render(request, "User/register.html", context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username atau password salah')

    context = {}
    return render(request, "User/login.html", context)

@allowed_users(allowed_roles=['admin', 'mahasiswa'])
def logoutUser(request):
    logout(request)
    return redirect('login')