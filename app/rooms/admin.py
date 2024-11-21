from django.contrib import admin
from .models import Sala, Reserva, Valoracion

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre",)

@admin.register(Valoracion)
class ValoracionAdmin(admin.ModelAdmin):
    list_display = ['satisfecho', 'fecha']
    list_filter = ['satisfecho', 'fecha']
    date_hierarchy = 'fecha'

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['sala', 'usuario', 'fecha', 'hora_inicio', 'hora_fin', 'estado']
    list_filter = ['estado', 'fecha', 'sala']
    search_fields = ['usuario__username', 'sala__nombre']
    actions = ['aprobar_reservas', 'denegar_reservas']

    def aprobar_reservas(self, request, queryset):
        queryset.update(estado='APROBADA')
    aprobar_reservas.short_description = "Aprobar reservas seleccionadas"

    def denegar_reservas(self, request, queryset):
        queryset.update(estado='RECHAZADA')
    denegar_reservas.short_description = "Denegar reservas seleccionadas"

    def save_model(self, request, obj, form, change):
        if not change:  # Si es una nueva reserva
            obj.estado = 'PENDIENTE'  # Establece el estado por defecto
        super().save_model(request, obj, form, change)
