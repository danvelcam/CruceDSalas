from django.urls import path
from . import views

urlpatterns = [
    path("salas/", views.lista_salas, name="lista_salas"),
    path("reserva-sala/<int:sala_id>/", views.reserva_sala, name="reserva_sala"),
    path("valoracion/", views.valorar_experiencia, name="valorar_experiencia"),
    path("mis-reservas/", views.mis_reservas, name="mis_reservas"),
    path(
        "cancelar-reserva/<int:reserva_id>/",
        views.cancelar_reserva,
        name="cancelar_reserva",
    ),
]
