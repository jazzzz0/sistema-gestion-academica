from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import NotRegistered
from django.forms.widgets import HiddenInput

from users.models import User, Admin


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


class AdminAdmin(admin.ModelAdmin):
    """
    Configuración del Django Admin para el modelo Admin.
    """
    # Columnas que se muestran en el listado
    list_display = (
        "dni",
        "name",
        "surname",
        "department",
        "hire_date",
        "user_is_active",
        "user_email",
    )
    
    # Filtros en la barra lateral
    list_filter = (
        "user__is_active",
        "department",
    )
    
    # Campos por los que se puede buscar
    search_fields = (
        "dni",
        "name",
        "surname",
        "user__email",
        "department",
    )
    
    # Organización de campos en el formulario
    fieldsets = (
        ("Información Personal", {
            "fields": (
                "dni",
                "name",
                "surname",
                "birth_date",
                "address",
                "phone",
            ),
        }),
        ("Información Laboral", {
            "fields": (
                "department",
                "hire_date",
            ),
        }),
        ("Usuario Asociado", {
            "fields": (
                "user",
            ),
            "description": "Usuario del sistema asociado a este administrador.",
        }),
    )
    
    # Ordenamiento por defecto
    ordering = ("-hire_date",)
    
    # Método para mostrar el email del usuario
    def user_email(self, obj):
        """Muestra el email del usuario asociado."""
        return obj.user.email if obj.user else "-"
    user_email.short_description = "Email"
    user_email.admin_order_field = "user__email"

    # Método para mostrar el estado de activación del usuario
    def user_is_active(self, obj):
        """Muestra el estado de activación del usuario asociado."""
        return obj.user.is_active if obj.user else "-"
    user_is_active.short_description = "Activo"
    user_is_active.admin_order_field = "user__is_active"
    user_is_active.boolean = True  # Muestra un ícono de checkmark/X en lugar de True/False

    # Acciones personalizadas
    actions = ["activate_admins", "deactivate_admins"]
    
    def activate_admins(self, request, queryset):
        """Activa los administradores seleccionados."""
        updated = 0
        for admin in queryset:
            if admin.user:
                admin.user.is_active = True
                admin.user.save(update_fields=['is_active'])
                updated += 1
        self.message_user(
            request,
            f"{updated} administrador(es) activado(s) correctamente.",
        )
    activate_admins.short_description = "Activar administradores seleccionados"
    
    def deactivate_admins(self, request, queryset):
        """Desactiva los administradores seleccionados."""
        updated = 0
        for admin in queryset:
            if admin.user:
                admin.user.is_active = False
                admin.user.save(update_fields=['is_active'])
                updated += 1
        self.message_user(
            request,
            f"{updated} administrador(es) desactivado(s) correctamente.",
        )
    deactivate_admins.short_description = "Desactivar administradores seleccionados"


# Desregistrar la clase UserAdmin por defecto (si existía) y registrar la personalizada
try:
    admin.site.unregister(User)
except NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)
admin.site.register(Admin, AdminAdmin)
