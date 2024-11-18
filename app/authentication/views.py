# autenticacion/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from app.authentication.forms import UserLoginForm, UserRegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data.get("dni")
            user = authenticate(request,dni=dni)
            if user is not None:
                msg = "Ya existe un usuario con ese DNI"
                return render(request, "auth/register.html", {"form": form, 'msg': msg})
            else:
                form.save()
            return redirect("home")
    else:
        form = UserRegisterForm()
    return render(request, "auth/register.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            surname = form.cleaned_data.get("surname")
            dni = form.cleaned_data.get("dni")
            user = authenticate(request, name=name, surname=surname, dni=dni)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                error = "Usuario o contraseña incorrectos"
                return render(request, "auth/login.html", {"form": form ,'error':error})
    else:
        form = UserLoginForm()
    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
    return redirect("home")
