from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.shortcuts import redirect


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


class SuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin para verificar que el usuario sea un Superusuario.

    Si el usuario no está logueado:
    Lo redirige al login.

    Si el usuario no es superusuario:
    Lo redirige al dashboard.
    """
    request: HttpRequest

    def test_func(self):
        """
        Comprueba si el usuario es superusuario
        """
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """
        Qué hacer si test_func() devuelve False.
        """
        # Si está logueado pero no es superusuario
        if self.request.user.is_authenticated:
            messages.error(self.request, "No tienes permiso para realizar esta acción.")
            return redirect('dashboard')

        # Si no está logueado, comportamiento estándar (login)
        return super().handle_no_permission()

class StudentRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin para verificar que el usuario sea un Estudiante.
    
    Si el usuario no está logueado:
    LoginRequiredMixin lo redirige al login.
    
    Si el usuario está logueado pero no es un Estudiante:
    UserPassesTestMixin falla y levanta un error 403 Permission Denied.
    """
    request: HttpRequest
    
    def test_func(self):
        """
        Comprobación de permisos
        """
        return self.request.user.role == "STUDENT"
    
    def handle_no_permission(self):
        """
        Qué hacer si test_func() devuelve False.
        """
        if self.request.user.is_authenticated:
            # Usuario logueado, pero no es un Estudiante, lanza un error 403
            messages.error(self.request, "No tienes permiso para realizar esta acción.")
            return redirect('dashboard')
        else:
            # Usuario no logueado, redirige al login
            return super().handle_no_permission()


class TeacherRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin para verificar que el usuario sea un Profesor.
    """
    request: HttpRequest

    def test_func(self):
        """
        Validamos contra el rol 'TEACHER' en el modelo User.
        """
        return self.request.user.role == "TEACHER"

    def handle_no_permission(self):
        """
        Manejo amigable del error de permisos.
        """
        if self.request.user.is_authenticated:
            # Si está logueado pero no es Profesor, lo redirigimos al dashboard con mensaje
            messages.error(self.request, "No tienes permisos de profesor para ver esta sección.")
            return redirect('dashboard')

        # Si no está logueado, lo manda al login
        return super().handle_no_permission()
