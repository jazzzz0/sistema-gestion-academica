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
    dni = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(choices=ROLE_CHOICES)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    force_password_change = models.BooleanField(default=False)

    # No usamos el campo "username" de AbstractUser
    username = None

    USERNAME_FIELD = "dni"
    REQUIRED_FIELDS = ["email", "first_name", "last_name", "role"]

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
