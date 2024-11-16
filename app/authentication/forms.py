# autenticacion/forms.py
from django import forms
import re
from .models import User


class UserLoginForm(forms.Form):
    Nombre = forms.CharField(label="Nombre")
    Apellidos = forms.CharField(label="Apellidos")
    DNI = forms.CharField(label="DNI")


class UserRegisterForm(forms.Form):
    Nombre = forms.CharField(label="Nombre")
    Apellidos = forms.CharField(label="Apellidos")
    DNI = forms.CharField(label="DNI")
    Email = forms.EmailField(label="Email")

    def clean_DNI(self):
        dni = self.cleaned_data.get("DNI")
        if not re.match(r"^\d{8}[A-Z]$", dni):
            raise forms.ValidationError("El DNI no ha sido ingresado correctamente")
        return dni

    def clean_Email(self):
        email = self.cleaned_data.get("Email")
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            self.add_error("DNI", "El DNI no ha sido ingresado correctamente")
        return email

    def save(self):
        data = self.cleaned_data
        User.objects.create_user(
            name=data.get("Nombre"),
            surname=data.get("Apellidos"),
            email=data.get("Email"),
            dni=data.get("DNI"),
        )
