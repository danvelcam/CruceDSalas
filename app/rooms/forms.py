from django import forms
from .models import Reserva
from django.utils import timezone
from datetime import timedelta, time

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha', 'hora_inicio', 'hora_fin','asunto']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'min': '09:00', 'max': '21:00'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'min': '09:00', 'max': '21:00'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')

        fecha_actual = timezone.now().date()
        fecha_limite = fecha_actual + timedelta(days=7)
        asunto = self.cleaned_data.get('asunto')
        if not asunto:
            raise forms.ValidationError("Este campo es obligatorio.")
        

        if fecha and (fecha < fecha_actual or fecha > fecha_limite):
            raise forms.ValidationError("La fecha debe estar entre hoy y los próximos 7 días.")

        if hora_inicio and hora_fin:
            hora_min = time(9, 0)  # 9:00 AM
            hora_max = time(21, 0)  # 9:00 PM

            if hora_inicio < hora_min or hora_inicio > hora_max:
                raise forms.ValidationError("La hora de inicio debe estar entre las 9:00 y las 21:00.")

            if hora_fin < hora_min or hora_fin > hora_max:
                raise forms.ValidationError("La hora de fin debe estar entre las 9:00 y las 21:00.")

            if hora_inicio >= hora_fin:
                raise forms.ValidationError("La hora de inicio debe ser anterior a la hora de fin.")

        return cleaned_data