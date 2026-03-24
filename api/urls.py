from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CanchaViewSet, ClienteViewSet, LoginView, LogoutView,
    MeView, RegisterView, ReservaViewSet, UserListView,
)

router = DefaultRouter()
router.register("clientes", ClienteViewSet)
router.register("canchas",  CanchaViewSet)
router.register("reservas", ReservaViewSet, basename="reserva")

urlpatterns = [
    path("",               include(router.urls)),
    path("auth/register/", RegisterView.as_view(),  name="auth-register"),
    path("auth/login/",    LoginView.as_view(),     name="auth-login"),
    path("auth/logout/",   LogoutView.as_view(),    name="auth-logout"),
    path("auth/me/",       MeView.as_view(),        name="auth-me"),
    path("admin/users/",   UserListView.as_view(),  name="admin-users"),
]
