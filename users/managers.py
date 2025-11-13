from typing import TYPE_CHECKING, Optional

from django.contrib.auth.models import UserManager as DjangoUserManager

if TYPE_CHECKING:
    from .models import User


class CustomUserManager(DjangoUserManager):
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
        # Validaciones básicas de integridad
        if not email:
            raise ValueError("El email debe ser proporcionado")
        if not role:
            raise ValueError("El rol debe ser proporcionado")

        allowed_roles = ("STUDENT", "TEACHER", "ADMIN")
        if role not in allowed_roles:
            raise ValueError(f"El rol debe ser uno de {', '.join(sorted(allowed_roles))}")

        email = self.normalize_email(email)

        # Configurar flags según el rol, superuser > admin > student/teacher
        if role in ("STUDENT", "TEACHER"):
            extra_fields.setdefault("is_staff", False)
            extra_fields.setdefault("is_superuser", False)
        elif role == "ADMIN":
            extra_fields.setdefault("is_staff", True)
            extra_fields.setdefault("is_superuser", False)

        user = self.model(email=email, role=role, **extra_fields)

        final_password: Optional[str] = None

        if role in ("STUDENT", "TEACHER"):
            if password:
                raise ValueError("Los estudiantes y los profesores no deben tener contraseñas manuales")
            if not dni:
                raise ValueError("Los estudiantes y los profesores deben tener un DNI")
            final_password = dni
            user.is_first_login = True

        elif role == "ADMIN":
            if not password:
                raise ValueError("Los administradores deben tener una contraseña establecida")
            final_password = password
            user.is_first_login = extra_fields.get("is_first_login", False)

        if not final_password:
            # Esto no debería ocurrir, pero es una medida de seguridad adicional
            raise ValueError("No se pudo determinar la contraseña final del usuario")

        # Guardar el usuario con la contraseña hasheada
        user.set_password(final_password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: Optional[str] = None,
        **extra_fields
    ) -> "User":
        """
        Crea un superusuario (único con is_superuser=True).
        Solo el superusuario puede acceder al Django Admin completo.
        """
        if not email:
            raise ValueError("El email debe ser proporcionado")
        if not password:
            raise ValueError("El superusuario debe tener una contraseña")

        # Asignar todos los flags de superusuario y el rol
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields["is_active"] = True
        extra_fields["role"] = "ADMIN"
        extra_fields["is_first_login"] = False

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
