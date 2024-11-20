from django.shortcuts import render, redirect
from .models import Sala
from .models import Valoracion


def lista_salas(request):
    salas = Sala.objects.all()
    return render(request, "rooms/lista_salas.html", {"salas": salas})


def reserva_sala(request, sala_id):
    sala = Sala.objects.get(id=sala_id)
    return render(request, "rooms/reserva_sala.html", {"sala": sala})

def valorar_experiencia(request):
    if request.method == 'POST':
        satisfecho = request.POST.get('valoracion') == 'positiva'
        Valoracion.objects.create(satisfecho=satisfecho)
        return redirect('lista_salas')
    
    return render(request, 'rooms/valoracion.html')
