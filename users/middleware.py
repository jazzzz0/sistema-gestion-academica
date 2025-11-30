from django.shortcuts import redirect
from django.urls import reverse, NoReverseMatch

from django.conf import settings


class ForcePasswordChangeMiddleware:
    """
    Middleware que fuerza a los usuarios a cambiar su contraseña si 'is_first_login' es True.
    Intercepta todas las peticiones excepto:
    1. La propia página de cambio de contraseña.
    2. La acción de cerrar sesión (logout).
    3. Archivos estáticos (CSS/JS) necesarios para renderizar la página.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Si no está autenticado, no hay nada que validar.
        if not request.user.is_authenticated:
            return self.get_response(request)

        # 2. Verificamos el flag del usuario de forma segura.
        # Si ya cambió la clave o el campo no existe, dejamos pasar.
        if not getattr(request.user, 'is_first_login', False):
            return self.get_response(request)

        # 3. Intentamos resolver las URLs protegidas.
        # Usamos try/except para evitar errores 500 si las rutas no cargaron aún.
        try:
            change_pass_url = reverse("users:first_login_change_password")
            # Ajusta "logout" o "users:logout" según cómo llames a tu ruta de salida
            logout_url = reverse("logout")
        except NoReverseMatch:
            return self.get_response(request)

        current_path = request.path

        # 4. Lógica de Bloqueo "El Guardián"
        # Si NO está en la página de cambio Y NO está saliendo...
        if current_path != change_pass_url and current_path != logout_url:

            # PERMITIR RECURSOS:
            # Es vital dejar pasar los estilos para que la página de error se vea bien.
            if settings.STATIC_URL and current_path.startswith(settings.STATIC_URL):
                return self.get_response(request)

            # BLOQUEO:
            return redirect(change_pass_url)

        return self.get_response(request)