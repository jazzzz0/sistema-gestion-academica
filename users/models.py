from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Administrator"),
        ("student", "Student"),
    ]

    # NOTA:
    # - El campo 'dni' se usará como USERNAME_FIELD.
    # - La contraseña inicial y la lógica para forzar el cambio se implementarán
    #   más adelante cuando hagamos el flujo completo de autenticación.
    # - Por ahora este modelo solo define la estructura y permite migraciones.
    dni = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="DNI",
        help_text="Documento Nacional de Identidad (único)",
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Correo electrónico (único)",
    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        max_length=10,
        verbose_name="Rol",
        help_text="Rol del usuario en el sistema",
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de alta",
        help_text="Fecha en que el usuario se unió al sistema",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si el usuario está activo",
    )
    force_password_change = models.BooleanField(
        default=False,
        verbose_name="Forzar cambio de contraseña",
        help_text="Indica si el usuario debe cambiar su contraseña en el próximo inicio de sesión",
    )

    # No usamos el campo "username" de AbstractUser
    username = None

    USERNAME_FIELD = "dni"
    REQUIRED_FIELDS = ["email", "first_name", "last_name", "role"]

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
