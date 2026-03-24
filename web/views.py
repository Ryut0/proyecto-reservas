from django.shortcuts import render


def canchas_list(request):
    return render(request, "web/canchas_list.html")

def login_view(request):
    return render(request, "web/login.html")

def register_view(request):
    return render(request, "web/register.html")

def reservas_list(request):
    return render(request, "web/reservas_list.html")

def reserva_form(request):
    return render(request, "web/reserva_form.html")

def admin_panel(request):
    return render(request, "web/admin_panel.html")
