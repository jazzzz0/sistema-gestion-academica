from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction

User = get_user_model()


class AuthService:
    """
    Servicio para manejar lógica compleja de autorización.
    """

    @staticmethod
    @transaction.atomic
    def complete_first_login_process(user: User, form: PasswordChangeForm) -> User:
        """
        Finaliza el proceso de primer login de forma atómica.
        """
        # Guardar la contraseña
        user_updated = form.save()

        # Actualizar el flag
        user_updated.is_first_login = False
        user_updated.save(update_fields=["is_first_login"])

        return user_updated
