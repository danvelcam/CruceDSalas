from django.shortcuts import render
from .models import Sala


def lista_salas(request):
    salas = Sala.objects.all()
    return render(request, "rooms/lista_salas.html", {"salas": salas})


def reserva_sala(request, sala_id):
    sala = Sala.objects.get(id=sala_id)
    return render(request, "rooms/reserva_sala.html", {"sala": sala})
