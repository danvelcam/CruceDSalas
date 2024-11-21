from django.db import models


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