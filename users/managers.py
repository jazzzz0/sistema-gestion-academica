from typing import TYPE_CHECKING, Optional

from django.contrib.auth.models import UserManager as DjangoUserManager

if TYPE_CHECKING:
    from .models import User


class CustomUserManager(DjangoUserManager):
    def _validate_common(self, email: str, role: str):
        """
        Validador común para ambos métodos de creación de usuarios.
        """
        if not email:
            raise ValueError("El email debe ser proporcionado")
        if not role:
            raise ValueError("El rol debe ser proporcionado")

        allowed_roles = ("STUDENT", "TEACHER", "ADMIN")
        if role not in allowed_roles:
            raise ValueError(f"El rol debe ser uno de {', '.join(sorted(allowed_roles))}")

    def create_user(
        self,
        username_ignored: str = None,
        email: str = None,
        dni: Optional[str] = None,
        role: str = None,
        password: Optional[str] = None,
        **extra_fields,
    ) -> "User":
        """
        Crear y guardar un usuario con políticas específicas según el rol:
        - STUDENT/TEACHER: la contraseña es el DNI. No existen contraseñas manuales. El campo 'is_first_login' es True.
        - ADMIN: la contraseña es manual. El campo 'is_first_login' es False.
        """
        # Validaciones
        self._validate_common(email, role)
        email = self.normalize_email(email)
        final_password: Optional[str] = None

        # Lógica de configuración agrupada por rol
        extra_fields.setdefault("is_superuser", False)  # Por defecto, ningún usuario es superusuario

        if role in ("STUDENT", "TEACHER"):
            # Configuración de permisos
            extra_fields.setdefault("is_staff", False)

            # Lógica de contraseña y login
            if password:
                raise ValueError("Estudiantes y profesores no deben tener contraseñas asignadas")
            if not dni:
                raise ValueError("El DNI es obligatorio para estudiantes y profesores")

            final_password = dni
            extra_fields["is_first_login"] = True

        elif role == "ADMIN":
            # Configuración de permisos
            extra_fields.setdefault("is_staff", True)

            # Lógica de contraseña y login
            if not password:
                raise ValueError("Los administradores deben tener una contraseña asignada")

            final_password = password
            extra_fields["is_first_login"] = False

        if not final_password:
            raise ValueError("No se pudo determinar la contraseña final")

        # Crear el usuario
        user = self.model(
            email=email,
            role=role,
            **extra_fields
        )

        user.set_password(final_password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        username_ignored: str = None,
        email: str = None,
        password: Optional[str] = None,
        **extra_fields
    ) -> "User":
        """
        Crea un superusuario.
        Este método delega la creación en create_user.
        Solo el superusuario puede acceder al Django Admin completo.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_first_login", False)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe ser staff")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe ser superusuario")

        # Forzar rol ADMIN para superusuarios
        return self.create_user(
            email=email,
            role="ADMIN",
            password=password,
            **extra_fields
        )
