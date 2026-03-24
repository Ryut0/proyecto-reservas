from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Cancha, Cliente, Reserva, UserProfile


# ── Clientes ──────────────────────────────────────────
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Cliente
        fields = ["id", "nombre", "email"]


# ── Canchas ───────────────────────────────────────────
class CanchaSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)
    imagen_url   = serializers.SerializerMethodField()

    class Meta:
        model  = Cancha
        fields = ["id", "nombre", "tipo", "tipo_display", "imagen", "imagen_url", "precio_por_hora"]
        extra_kwargs = {"imagen": {"required": False, "allow_null": True}}

    def get_imagen_url(self, obj):
        if obj.imagen:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.imagen.url)
            return obj.imagen.url
        return None


# ── Reservas ──────────────────────────────────────────
class ReservaSerializer(serializers.ModelSerializer):
    cliente_nombre      = serializers.CharField(source="cliente.nombre",          read_only=True)
    cancha_nombre       = serializers.CharField(source="cancha.nombre",           read_only=True)
    cancha_tipo         = serializers.CharField(source="cancha.get_tipo_display", read_only=True)
    cancha_tipo_key     = serializers.CharField(source="cancha.tipo",             read_only=True)
    cancha_imagen_url   = serializers.SerializerMethodField()
    creado_por_username = serializers.CharField(source="creado_por.username",     read_only=True)
    precio_total        = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model  = Reserva
        fields = [
            "id", "cliente", "cliente_nombre",
            "cancha", "cancha_nombre", "cancha_tipo", "cancha_tipo_key", "cancha_imagen_url",
            "fecha", "hora_inicio", "hora_fin",
            "precio_total",
            "creado_por", "creado_por_username",
        ]
        read_only_fields = ["creado_por", "precio_total"]
        extra_kwargs = {
            "cliente": {"required": False, "allow_null": True}
        }

    def get_cancha_imagen_url(self, obj):
        if obj.cancha.imagen:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.cancha.imagen.url)
            return obj.cancha.imagen.url
        return None

    def validate(self, attrs):
        hora_inicio = attrs.get("hora_inicio") or getattr(self.instance, "hora_inicio", None)
        hora_fin    = attrs.get("hora_fin")    or getattr(self.instance, "hora_fin",    None)
        cancha      = attrs.get("cancha")      or getattr(self.instance, "cancha",      None)
        fecha       = attrs.get("fecha")       or getattr(self.instance, "fecha",       None)

        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise serializers.ValidationError(
                {"hora_fin": "La hora de fin debe ser mayor que la hora de inicio."}
            )
        if cancha and fecha and hora_inicio and hora_fin:
            overlapping = (
                Reserva.objects.filter(cancha=cancha, fecha=fecha)
                .exclude(pk=getattr(self.instance, "pk", None))
                .filter(hora_inicio__lt=hora_fin, hora_fin__gt=hora_inicio)
            )
            if overlapping.exists():
                raise serializers.ValidationError(
                    {"cancha": "La cancha ya tiene una reserva en ese horario."}
                )
        return attrs


# ── Registro ──────────────────────────────────────────
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    role     = serializers.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        default="usuario", write_only=True, required=False,
    )

    class Meta:
        model  = User
        fields = ["id", "username", "email", "password", "role"]

    def create(self, validated_data):
        role = validated_data.pop("role", "usuario")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        UserProfile.objects.create(user=user, role=role)
        return user


# ── Perfil ────────────────────────────────────────────
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email    = serializers.CharField(source="user.email",    read_only=True)
    is_staff = serializers.BooleanField(source="user.is_staff", read_only=True)

    class Meta:
        model  = UserProfile
        fields = ["username", "email", "role", "is_staff"]
