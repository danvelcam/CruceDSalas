# autenticacion/views.py
from random import randint
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from app.authentication.forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from app.utils.crypto import encrypt_cbc, key
from app.authentication.models import User
from django.contrib import messages
import datetime


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data.get("dni")
            dni_coded = encrypt_cbc(dni, key)
            try:
                if User.objects.filter(dni=dni_coded).exists():
                    messages.warning(request, "Ya existe un usuario con ese DNI")
                    return render(request, "auth/register.html", {"form": form})
                form.save()
                messages.success(request, "Usuario creado exitosamente")
                return redirect("home")
            except Exception as e:
                messages.error(request, f"Ha ocurrido un error: {e}")
    else:
        form = UserRegisterForm()
    return render(request, "auth/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("lista_salas")

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            pin = form.cleaned_data.get("pin")
            dni = form.cleaned_data.get("dni")
            user = authenticate(request, username=dni, password=pin)
            if user is not None:
                login(request, user)
                return redirect("lista_salas")
            else:
                error = "Usuario o contraseña incorrectos"
                return render(
                    request, "auth/login.html", {"form": form, "error": error}
                )
    else:
        form = UserLoginForm()

    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
    return redirect("home")


def send_verification_code(request):
    if request.method == "POST":
        try:
            phone = request.POST.get("phone_number")
            coded_phone = encrypt_cbc(phone, key)
            user = User.objects.get(tlf=coded_phone)
            code = randint(1000, 9999)
            request.session["code"] = code
            request.session["user_id"] = user.id
            _sms_pin_generator(code, phone)
            return redirect("verify_code")
        except User.DoesNotExist:
            error = "No se ha encontrado el usuario asociado a dicho teléfono"
            return render(request, "auth/send_verification_code.html", {"error": error})
    return render(request, "auth/send_verification_code.html")


def verify_code(request):
    if request.method == "POST":
        given_code = request.POST.get("verification_code")
        if given_code == str(request.session["code"]):
            user = User.objects.get(id=request.session["user_id"])
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            return redirect("password_reset_confirm", uidb64=uid, token=token)
    return render(request, "auth/verify_code.html")


def password_reset_confirm(request, uidb64, token):
    if request.method == "POST":
        new_pin = request.POST.get("new_pin")
        user_id = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.set_password(new_pin)
            user.save()
            messages.success(request, "Tu contraseña ha sido cambiada exitosamente.")
        return redirect("home")
    return render(request, "auth/password_reset_confirm_custom.html")


def _sms_pin_generator(pin, tlf):
    file_path = "sms.log"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"Your recovery code is {pin}"
    log_entry = f'[{timestamp}] To: {tlf} | Message: "{message}" \n'
    with open(file_path, "a") as file:
        file.write(log_entry)
