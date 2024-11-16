from django.db import models


class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="salas/")

    def __str__(self):
        return self.nombre
