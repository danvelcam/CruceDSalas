from django.contrib import admin
from .models import Sala
from .models import Valoracion

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre",)

@admin.register(Valoracion)
class ValoracionAdmin(admin.ModelAdmin):
    list_display = ['satisfecho', 'fecha']
    list_filter = ['satisfecho', 'fecha']
    date_hierarchy = 'fecha'
