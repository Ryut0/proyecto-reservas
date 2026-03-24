from django.contrib import admin

from .models import Cancha, Cliente, Reserva


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display  = ("nombre", "email")
    search_fields = ("nombre", "email")


@admin.register(Cancha)
class CanchaAdmin(admin.ModelAdmin):
    list_display  = ("nombre", "tipo", "precio_por_hora")
    list_filter   = ("tipo",)
    search_fields = ("nombre",)


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display  = ("creado_por", "cancha", "fecha", "hora_inicio", "hora_fin", "precio_total")
    list_filter   = ("fecha", "cancha")
    search_fields = ("creado_por__username", "cancha__nombre")
    readonly_fields = ("precio_total",)
