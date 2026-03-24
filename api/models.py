from django.contrib.auth.models import User
from django.db import models


# ── Perfil de usuario con rol ─────────────────────────
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("admin",   "Administrador"),
        ("usuario", "Usuario"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="usuario")

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == "admin"


# ── Clientes ──────────────────────────────────────────
class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    email  = models.EmailField(unique=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} <{self.email}>"


# ── Canchas ───────────────────────────────────────────
class Cancha(models.Model):
    TIPO_CHOICES = [
        ("futbol",     "Fútbol"),
        ("tenis",      "Tenis"),
        ("baloncesto", "Baloncesto"),
        ("voleibol",   "Voleibol"),
        ("padel",      "Pádel"),
        ("otro",       "Otro"),
    ]
    nombre          = models.CharField(max_length=120)
    tipo            = models.CharField(max_length=20, choices=TIPO_CHOICES)
    imagen          = models.ImageField(
        upload_to="canchas/",
        null=True, blank=True,
        help_text="Foto de la cancha (opcional)"
    )
    precio_por_hora = models.DecimalField(
        max_digits=8, decimal_places=2,
        default=30000,
        help_text="Precio por hora en COP"
    )

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


# ── Reservas ──────────────────────────────────────────
class Reserva(models.Model):
    cliente      = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name="reservas")
    cancha       = models.ForeignKey(Cancha,  on_delete=models.CASCADE, related_name="reservas")
    fecha        = models.DateField()
    hora_inicio  = models.TimeField()
    hora_fin     = models.TimeField()
    precio_total = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    creado_por   = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="reservas_creadas"
    )

    class Meta:
        ordering = ["-fecha", "hora_inicio"]

    def __str__(self):
        return f"{self.cancha} - {self.fecha} {self.hora_inicio}-{self.hora_fin}"
