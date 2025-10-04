from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser de Django.
    """

    ROLE_CHOICES = [
        ("ADMIN", "Administrador"),
        ("STUDENT", "Alumno"),
        ("TEACHER", "Profesor"),
    ]

    # NOTA:
    # - El email se usará como USERNAME_FIELD.
    # - La contraseña inicial se seteará con el DNI de la Persona asociada.
    # - Esto se implementará en un UserManager personalizado,
    #   que usará set_password() para guardar la contraseña hasheada.

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

    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si el usuario está activo",
    )

    is_first_login = models.BooleanField(
        default=True,
        verbose_name="Forzar cambio de contraseña",
        help_text=(
            "Indica si el usuario debe cambiar su contraseña "
            "en el próximo inicio de sesión"
        ),
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de alta",
        help_text="Fecha en que el usuario se unió al sistema",
    )

    # No usamos el campo "username" de AbstractUser
    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["role"]

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"
