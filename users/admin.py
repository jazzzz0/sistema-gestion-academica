from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import NotRegistered
from django.forms.widgets import HiddenInput

from users.models import User


class CustomUserAdmin(UserAdmin):
    # Columnas que se muestran en el listado
    list_display = ("email", "role", "is_staff", "is_superuser", "is_active", "date_joined")
    search_fields = ("email", "role")
    ordering = ("email",)

    # Campos de solo lectura
    readonly_fields = ("last_login", "date_joined")

    # Campos que se muestran en el formulario de edición
    fieldsets = (
        # Identidad del usuario
        (None,
            {"fields": ("email", "password")}),
        ("Estado y Rol",
            {"fields": ('role', "is_active", 'is_first_login')}),
        ("Permisos de Sistema y Grupos",
            {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Registro de Fechas",
            {"fields": ("last_login", "date_joined")}),
    )

    # Campos para crear un nuevo usuario
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
        ("Estado y Rol",
            {"fields": ('role', "is_active", 'is_first_login')}),
        ("Permisos de Sistema y Grupos",
            {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    # REGLA DE SEGURIDAD: Solo Superusers pueden crear/editar Admins
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Restricción principal: Si el usuario no es superuser
        if not request.user.is_superuser:
            role_choices = getattr(User, "ROLE_CHOICES", [])
            if role_choices and "role" in form.base_fields:
                choices = [c for c in role_choices if c[0] != "ADMIN"]
                form.base_fields["role"].choices = choices  # type: ignore[attr-defined]

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
