from django.shortcuts import render, redirect
from .models import Sala
from .models import Valoracion
from django.contrib import messages

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
        messages.success(request, '¡Gracias! Tu valoración se ha enviado con éxito.')  # Mensaje de éxito
        return redirect('lista_salas')  # Redirige después de guardar la valoración

    return render(request, 'rooms/valoracion.html')