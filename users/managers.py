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
        # Validaciones básicas de integridad
        if not email:
            raise ValueError("El email debe ser proporcionado")
        if not role:
            raise ValueError("El rol debe ser proporcionado")

        email = self.normalize_email(email)

        # Se asegura que los flags de permisos sean False por defecto
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(email=email, role=role, **extra_fields)

        # Lógica de contraseña y primer login
        final_password: str = ""  # Inicializamos para evitar errores de referencia
        is_manual_password = bool(password)

        if role in ("STUDENT", "TEACHER"):
            if not is_manual_password:
                # Si no se provee contraseña, usar el DNI
                if not dni:
                    raise ValueError("El DNI debe ser proporcionado para roles STUDENT o TEACHER")
                final_password = dni
                user.is_first_login = True  # Forzar cambio de contraseña en el primer login
            else:
                final_password = password
                user.is_first_login = extra_fields.get("is_first_login", False)

        elif role == "ADMIN":
            if not is_manual_password:
                # Rol ADMIN (no Superuser): Debe tener una contraseña manual segura.
                # Medida de seguridad que impide crear Admins sin contraseña.
                raise ValueError("El rol ADMIN requiere una contraseña manual establecida")
            else:
                final_password = password
                user.is_first_login = extra_fields.get("is_first_login", False)

        # Usar set_password para hashear la contraseña
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
        Crea un superusuario directamente, sin la lógica de DNI, y asigna 'ADMIN'.
        """
        if not email:
            raise ValueError("El email debe ser proporcionado")

        # 1. Asignar todos los flags de superusuario y el rol
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)  # Asegurar que esté activo
        extra_fields.setdefault("role", "ADMIN")
        extra_fields.setdefault("is_first_login", False)  # No forzar cambio de contraseña

        # 2. Verificar seguridad
        if not extra_fields.get("is_staff"):
            raise ValueError("El superusuario debe tener is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("El superusuario debe tener is_superuser=True.")

        # 3. Crear el objeto User directamente, evitando la dependencia de create_user(dni)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        # Si no se pasó contraseña, Django lo obligará en el prompt.
        if not password:
            raise ValueError("El superusuario debe tener una contraseña establecida.")

        user.set_password(password)

        # 4. Guardar
        user.save(using=self._db)
        return user
