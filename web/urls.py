from django.urls import path
from . import views

urlpatterns = [
    path("",                views.canchas_list,  name="canchas-list"),
    path("login/",          views.login_view,    name="login"),
    path("registro/",       views.register_view, name="register"),
    path("reservas/",       views.reservas_list, name="reservas-list"),
    path("reservas/nueva/", views.reserva_form,  name="reserva-form"),
    path("admin-panel/",    views.admin_panel,   name="admin-panel"),
]
