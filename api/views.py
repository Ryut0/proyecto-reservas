from datetime import datetime, date
from decimal import Decimal

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cancha, Cliente, Reserva, UserProfile
from .serializers import (
    CanchaSerializer, ClienteSerializer, ReservaSerializer,
    UserProfileSerializer, UserRegisterSerializer,
)


# ── Permiso: solo admin ───────────────────────────────
class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        try:
            return request.user.profile.is_admin
        except UserProfile.DoesNotExist:
            return False


# ── Clientes ──────────────────────────────────────────
class ClienteViewSet(viewsets.ModelViewSet):
    queryset         = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        return [IsAdminRole()]


# ── Canchas ───────────────────────────────────────────
class CanchaViewSet(viewsets.ModelViewSet):
    queryset         = Cancha.objects.all()
    serializer_class = CanchaSerializer
    parser_classes   = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        return [IsAdminRole()]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


# ── Reservas ──────────────────────────────────────────
class ReservaViewSet(viewsets.ModelViewSet):
    serializer_class   = ReservaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Reserva.objects.select_related("cliente", "cancha", "creado_por").all()
        try:
            if user.profile.is_admin:
                return Reserva.objects.select_related("cliente", "cancha", "creado_por").all()
        except UserProfile.DoesNotExist:
            pass
        return Reserva.objects.select_related("cliente", "cancha", "creado_por").filter(creado_por=self.request.user)

    def get_permissions(self):
        if self.action in ("destroy", "update", "partial_update"):
            return [IsAdminRole()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        cancha      = serializer.validated_data["cancha"]
        hora_inicio = serializer.validated_data["hora_inicio"]
        hora_fin    = serializer.validated_data["hora_fin"]

        # Calcular horas (si se pasa de medianoche también lo maneja)
        inicio_dt = datetime.combine(date.today(), hora_inicio)
        fin_dt    = datetime.combine(date.today(), hora_fin)
        segundos  = (fin_dt - inicio_dt).seconds
        horas     = Decimal(str(round(segundos / 3600, 6)))

        precio_total = round(horas * cancha.precio_por_hora, 2)

        # Buscar o crear un Cliente vinculado al usuario logueado
        user = self.request.user
        email = user.email or f"{user.username}@reservas.com"
        cliente, _ = Cliente.objects.get_or_create(
            email=email,
            defaults={"nombre": user.get_full_name() or user.username}
        )

        serializer.save(creado_por=user, cliente=cliente, precio_total=precio_total)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


# ── Registro ──────────────────────────────────────────
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        requested_role = request.data.get("role", "usuario")
        if requested_role == "admin":
            if not request.user.is_authenticated:
                return Response({"detail": "Solo un administrador puede crear cuentas de admin."}, status=403)
            try:
                if not request.user.is_staff and not request.user.profile.is_admin:
                    return Response({"detail": "Solo un administrador puede crear cuentas de admin."}, status=403)
            except UserProfile.DoesNotExist:
                return Response({"detail": "Solo un administrador puede crear cuentas de admin."}, status=403)

        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user     = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            try:
                role = user.profile.role
            except UserProfile.DoesNotExist:
                role = "usuario"
            return Response({"token": token.key, "role": role, "username": user.username}, status=201)
        return Response(serializer.errors, status=400)


# ── Login ─────────────────────────────────────────────
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"detail": "username y password son requeridos."}, status=400)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"detail": "Credenciales inválidas."}, status=401)
        token, _ = Token.objects.get_or_create(user=user)
        role = "usuario"
        if user.is_staff:
            role = "admin"
        else:
            try:
                role = user.profile.role
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(user=user, role="usuario")
        return Response({"token": token.key, "role": role, "username": user.username})


# ── Logout ────────────────────────────────────────────
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({"detail": "Sesión cerrada."})


# ── Me ────────────────────────────────────────────────
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        role = "admin" if user.is_staff else "usuario"
        try:
            role = user.profile.role
        except UserProfile.DoesNotExist:
            pass
        return Response({"username": user.username, "email": user.email, "role": role, "is_staff": user.is_staff})


# ── Usuarios (admin) ──────────────────────────────────
class UserListView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        users = User.objects.select_related("profile").all()
        data  = []
        for u in users:
            try:
                role = u.profile.role
            except UserProfile.DoesNotExist:
                role = "admin" if u.is_staff else "usuario"
            data.append({"id": u.id, "username": u.username, "email": u.email,
                         "role": role, "is_staff": u.is_staff, "is_active": u.is_active})
        return Response(data)

    def patch(self, request):
        user_id  = request.data.get("user_id")
        new_role = request.data.get("role")
        if not user_id or new_role not in ("admin", "usuario"):
            return Response({"detail": "Datos inválidos."}, status=400)
        try:
            target = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Usuario no encontrado."}, status=404)
        profile, _ = UserProfile.objects.get_or_create(user=target)
        profile.role = new_role
        profile.save()
        return Response({"detail": f"Rol actualizado a {new_role}."})
