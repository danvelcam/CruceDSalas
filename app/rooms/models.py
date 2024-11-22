from django.db import models
from app.authentication.models import User
from django.utils import timezone
from datetime import timedelta


class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="salas/")

    def __str__(self):
        return self.nombre


class Valoracion(models.Model):
    satisfecho = models.BooleanField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Valoración {'👍' if self.satisfecho else '👎'} - {self.fecha}"


class Reserva(models.Model):
    ESTADO_CHOICES = [
        ("PENDIENTE", "Pendiente de aprobación"),
        ("APROBADA", "Aprobada"),
        ("RECHAZADA", "Rechazada"),
    ]

    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default="PENDIENTE"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    asunto = models.CharField(
        max_length=255, verbose_name="Asunto de la reserva", default="No especificado"
    )

    def __str__(self):
        return f"Reserva de {self.sala} por {self.usuario} el {self.fecha}"

    class Meta:
        ordering = ["fecha", "hora_inicio"]
