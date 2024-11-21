from django.urls import path
from . import views

urlpatterns = [
    path("salas/", views.lista_salas, name="lista_salas"),
    path("salas/<int:sala_id>/reserva/", views.reserva_sala, name="reserva_sala"),
    path('valoracion/', views.valorar_experiencia, name='valorar_experiencia'),
]
