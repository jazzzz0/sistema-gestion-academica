from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import CustomUserManager


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

    is_first_login = models.BooleanField(
        default=True,
        verbose_name="Forzar cambio de contraseña",
        help_text=(
            "Indica si el usuario debe cambiar su contraseña "
            "en el próximo inicio de sesión"
        ),
    )

    # No usamos el campo "username" de AbstractUser.
    # Los campos first_name y last_name se gestionarán
    # a través del modelo Persona asociado (name y surname).
    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # No requerimos role al crear superusuario, siempre será ADMIN

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"

    @property
    def full_name_display(self):
        """
        Retorna el nombre real desde el perfil asociado.
        Si no existe, retorna el email.
        """
        name = self.email
        is_email = True

        try:
            if self.role == 'STUDENT' and hasattr(self, 'student_profile'):
                name = self.student_profile.get_full_name()
                is_email = False

            elif self.role == 'TEACHER' and hasattr(self, 'teacher_profile'):
                name = self.teacher_profile.get_full_name()
                is_email = False

            elif self.role == 'ADMIN' and hasattr(self, 'admin_profile'):
                name = self.admin_profile.get_full_name()
                is_email = False

        except Exception:
            pass

        if is_email:
            return name

        return name.title()
