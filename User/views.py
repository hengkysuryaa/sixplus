from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

from User.forms import CreateUserForm
from User.decorators import *

@authenticated_user
def dashboard(request):
    context = {}
    if(len(request.user.groups.filter(name = "dosen")) == 1):
        print("This is dosen")
        return redirect("dosen:Home", nip = request.user.first_name)
    elif(len(request.user.groups.filter(name = "tu")) == 1):
        print("This is tu")
    elif(len(request.user.groups.filter(name = "mahasiswa")) == 1):
        print("This is mahasiswa")
        return redirect("mhs:Home", nim = request.user.first_name)
    return render(request, "User/dashboard.html", context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            nimp = form.cleaned_data.get('first_name') #nimp = nip / nim
            messages.success(request, f'Akun {username} berhasil dibuat')
            if len(nimp) == 8: 
                group = Group.objects.get(name = 'mahasiswa')
            elif len(nimp) > 8:
                group = Group.objects.get(name = 'dosen')
            else:
                group = Group.objects.get(name = 'tu')
            user.groups.add(group)
            return redirect('login')
    
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

def logoutUser(request):
    logout(request)
    return redirect('login')