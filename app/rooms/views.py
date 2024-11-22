from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Sala, Reserva, Valoracion
from .forms import ReservaForm
from django.utils import timezone
from datetime import timedelta

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

@login_required
def reserva_sala(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)
    fecha_actual = timezone.now().date()
    fecha_limite = fecha_actual + timedelta(days=7)

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.sala = sala
            reserva.usuario = request.user
            reserva.save()
            return redirect('valorar_experiencia')  # O a donde quieras redirigir después de la reserva
    else:
        form = ReservaForm(initial={'fecha': fecha_actual})

    return render(request, 'rooms/reserva_sala.html', {
        'form': form,
        'sala': sala,
        'fecha_actual': fecha_actual,
        'fecha_limite': fecha_limite,
    })

def mis_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'rooms/mis_reservas.html', {'reservas': reservas})
