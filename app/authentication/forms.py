from django import forms
import re
from app.authentication.models import User


class UserLoginForm(forms.Form):
    dni = forms.CharField(label="DNI")
    pin = forms.CharField(label="PIN", widget=forms.PasswordInput)

    # def clean_dni(self):
    #     dni = self.cleaned_data.get("dni")
    #     if not re.match(r"^\d{8}[A-Z]$", dni):
    #         raise forms.ValidationError("El DNI no ha sido ingresado correctamente")
    #     if not _check_DNI(dni):
    #         raise forms.ValidationError("El DNI no es válido")
    #     return dni


class UserRegisterForm(forms.Form):
    name = forms.CharField(label="Nombre")
    surname = forms.CharField(label="Apellidos")
    dni = forms.CharField(label="DNI")
    email = forms.EmailField(label="Email")
    tlf= forms.CharField(label="Teléfono")
    choose_pin = forms.BooleanField(label="Deseo elegir mi propio PIN", required=False)
    pin = forms.CharField(label="PIN", widget=forms.PasswordInput, required=False)
    accept_terms = forms.BooleanField(label="Acepto el almacenamiento de mis datos", required=True)


    def clean_dni(self):
        dni = self.cleaned_data.get("dni")
        if not re.match(r"^\d{8}[A-Z]$", dni):
            raise forms.ValidationError("El DNI no ha sido ingresado correctamente")
        if not _check_DNI(dni):
            raise forms.ValidationError("El DNI no es válido")
        return dni
    
    def clean(self):
        cleaned_data = super().clean()
        choose_pin = cleaned_data.get("choose_pin")
        pin = cleaned_data.get("pin")

        if choose_pin and not pin:
            raise forms.ValidationError("Debe ingresar un PIN si ha seleccionado la opción de elegir su propio PIN.")
        return cleaned_data

    def clean_email(self) -> str:
        email = self.cleaned_data.get("email")
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            self.add_error("DNI", "El DNI no ha sido ingresado correctamente")
        return email

    def save(self):
        data = self.cleaned_data
        User.objects.create_user(
            name=data.get("name"),
            surname=data.get("surname"),
            email=data.get("email"),
            dni=data.get("dni"),
            tlf=data.get("tlf"),
            pin=data.get("pin") if data.get("choose_pin") else None
        )

def _check_DNI(dni:str ) -> bool:
        control_letter = {
    0: 'T', 1: 'R', 2: 'W', 3: 'A', 4: 'G', 5: 'M', 6: 'Y', 7: 'F', 8: 'P', 9: 'D',
    10: 'X', 11: 'B', 12: 'N', 13: 'J', 14: 'Z', 15: 'S', 16: 'Q', 17: 'V', 18: 'H', 19: 'L',
    20: 'C', 21: 'K', 22: 'E'
}
        dni_letter = dni[-1]
        dni_numbers = int(dni[:-1])
        return control_letter[dni_numbers % 23] == dni_letter

