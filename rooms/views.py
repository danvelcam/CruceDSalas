from django.shortcuts import render
from .models import Sala

def lista_salas(request):
    salas = Sala.objects.all()
    return render(request, 'salas/lista_salas.html', {'salas': salas})

def reserva_sala(request, sala_id):
    sala = Sala.objects.get(id=sala_id)
    return render(request, 'salas/reserva_sala.html', {'sala': sala})