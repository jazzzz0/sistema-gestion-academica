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
        Crea y guarda un usuario con el email, DNI, rol y contraseña proporcionados.
        """
        if not email:
            raise ValueError("El email debe ser proporcionado")
        if not role:
            raise ValueError("El rol debe ser proporcionado")

        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)

        is_manual_password = bool(password)

        # Lógica de Contraseña y Primer Login
        # TODO: Terminar esta lógica

        if role in ("STUDENT", "TEACHER") or not is_manual_password:
            if not dni:
                raise ValueError(
                    "El DNI debe ser proporcionado para alumnos y profesores"
                )
            # Alumnos y Profesores sin contraseña manual:
            # usar DNI y forzar cambio.
            final_password = dni
            user.is_first_login = True
        elif role == "ADMIN" and not is_manual_password:

        user.set_password(final_password)

        # Lógica de permisos
        # Solo se establece a True si se recibe desde create_superuser
        user.is_staff = extra_fields.get("is_staff", False)
        user.is_superuser = extra_fields.get("is_superuser", False)

        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: Optional[str] = None, **extra_fields
    ) -> "User":
        """
        Crea un superusuario directamente, sin la lógica de DNI, y asigna 'ADMIN'.
        """
        if not email:
            raise ValueError("El email debe ser proporcionado")

        # 1. Asignar todos los flags de superusuario y el rol
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)  # Asegurar que esté activo
        extra_fields.setdefault("role", "ADMIN")
        extra_fields.setdefault(
            "is_first_login", False
        )  # No forzar cambio de contraseña

        # 2. Verificar seguridad
        if not extra_fields.get("is_staff"):
            raise ValueError("El superusuario debe tener is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("El superusuario debe tener is_superuser=True.")

        # 3. Crear el objeto User directamente, usando el password.
        email = self.normalize_email(email)

        # Creamos el modelo. Django se encarga de que password esté hasheado.
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        # 4. Guardar
        user.save(using=self._db)
        return user
