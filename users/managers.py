from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, dni, role, password=None, **extra_fields):
        """
        Crea un usuario con email, persona y rol.
        La contraseña inicial se establece con el DNI de la persona asociada.
        """
        if not email:
            raise ValueError("El email debe ser proporcionado")
        if not dni:
            raise ValueError("El DNI debe ser proporcionado")
        if not role:
            raise ValueError("El rol debe ser proporcionado")

        email = self.normalize_email(email)
        user = self.model(email=email, dni=dni, role=role, **extra_fields)

        # Contraseña inicial = DNI
        # Usamos set_password para hashear la contraseña
        user.set_password(dni)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, dni, password=None, **extra_fields):
        """
        Crea y guarda un superusuario (admin total del sistema).
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")  # Aseguramos que el rol sea 'admin'

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True")

        if password:
            user.set_password(password)
        else:
            user.set_password(dni)

        return self.create_user(
            email=email, dni=dni, role="admin", password=password, **extra_fields
        )
