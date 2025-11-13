from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import NotRegistered
from django.forms.widgets import HiddenInput

from subjects.models import Subject
from users.models import User
from users.models.teacher import Teacher


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
            {"fields": ("role", "is_active", "is_first_login")}),
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
            {"fields": ("role", "is_active", "is_first_login")}),
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


class SubjectTeacherInline(admin.TabularInline):
    """
    Inline para mostrar las materias asignadas a un profesor.
    """
    model = Subject
    fk_name = "teacher"
    fields = ("name",)
    readonly_fields = ("name",)
    extra = 0
    # Impedir añadir o eliminar asignaciones
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Teacher.
    """
    list_display = ("full_name", "dni", "academic_degree", "subject_count", "hire_date", "is_active")
    list_filter = ("user__is_active", "academic_degree", "hire_date")
    search_fields = ("name", "surname", "dni", "user__email")
    inlines = [SubjectTeacherInline]

    fieldsets = (
        ("Información Personal", {
            "fields": ("name", "surname", "dni", "birth_date", "address", "phone")
        }),
        ("Información Académica", {
            "fields": ("academic_degree",)
        }),
        ("Información Laboral", {
           "fields": ("hire_date",)
        }),
    )

    readonly_fields = ("user",)

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    full_name.short_description = "Nombre Completo"

    def subject_count(self, obj):
        return obj.subjects.count() if obj.user else 0
    subject_count.short_description = "N° de Materias"

    def is_active(self, obj):
        return obj.user.is_active if obj.user else False
    is_active.boolean = True
    is_active.short_description = "Estado"


# Desregistrar la clase UserAdmin por defecto (si existía) y registrar la personalizada
try:
    admin.site.unregister(User)
except NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)
