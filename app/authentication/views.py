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
            pin = form.cleaned_data.get("pin")
            dni = form.cleaned_data.get("dni")
            print(dni, pin)
            user = authenticate(request, username=dni, password = pin)
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
