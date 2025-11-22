from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.urls import reverse


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin para verificar que el usuario sea un Administrador.

    Si el usuario no está logueado:
    LoginRequiredMixin lo redirige al login.

    Si el usuario está logueado pero no es un Administrador:
    UserPassesTestMixin falla y levanta un error 403 Permission Denied.
    """
    request: HttpRequest

    def test_func(self):
        """
        Comprobación de permisos
        """
        return self.request.user.role == "ADMIN"

    def handle_no_permission(self):
        """
        Qué hacer si test_func() devuelve False.
        """
        if self.request.user.is_authenticated:
            # Usuario logueado, pero no es un Administrador, lanza un error 403
            raise PermissionDenied
        else:
            # Usuario no logueado, redirige al login
            return super().handle_no_permission()
