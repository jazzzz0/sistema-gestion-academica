from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import NotRegistered
from django.forms.widgets import HiddenInput
from .models import User


class CustomUserAdmin(UserAdmin):
    # Campos que se muestran en el formulario de edición
    fieldsets = (
        # Identidad del usuario
        (None, {"fields": ("email", "password")}),
        # Control de acceso y rol
        ("Información personal", {"fields": ('role', 'is_first_login')}),
        ("Permisos de Sistema", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Fechas Importantes", {"fields": ("last_login", "date_joined")}),
    )

    # Columnas que se muestran en el listado
    list_display = ("email", "role", "is_staff", "is_superuser", "is_active", "date_joined")
    search_fields = ("email", "role")
    ordering = ("email",)

    # REGLA DE SEGURIDAD: Solo Superusers pueden crear/editar Admins
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Restricción principal: Si el usuario no es superuser
        if not request.user.is_superuser:
            # Restringir el campo "role" para que no se pueda asignar "ADMIN"
            choices = [c for c in User.ROLE_CHOICES if c[0] != "ADMIN"]
            form.base_fields["role"].choices = choices  # type: ignore

            # Ocultar los flags críticos de permisos para evitar manipulaciones
            if "is_staff" in form.base_fields:
                form.base_fields["is_staff"].widget = HiddenInput()
            if "is_superuser" in form.base_fields:
                form.base_fields["is_superuser"].widget = HiddenInput()

        return form


# Desregistrar la clase UserAdmin por defecto (si existía) y registrar la personalizada
try:
    admin.site.unregister(User)
except NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)
