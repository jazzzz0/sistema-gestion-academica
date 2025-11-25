import re

from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

from users.services.admin_service import AdminService


class AdminCreateForm(forms.Form):
    """
    Formulario personalizado para la creación de usuarios Admin.
    """
    # Campos Person obligatorios
    name = forms.CharField(
        max_length=100,
        label="Nombre",
        help_text="Nombre del Administrador",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre'}),
    )
    surname = forms.CharField(
        max_length=100,
        label="Apellido",
        help_text="Apellido del Administrador",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el apellido'}),
    )
    dni = forms.CharField(
        max_length=10,
        label="DNI",
        help_text="Documento Nacional de Identidad (único)",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12345678'}),
    )

    # Campos Person opcionales
    address = forms.CharField(
        max_length=200,
        label="Domicilio",
        help_text="Domicilio (opcional)",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el domicilio'}),
    )
    birth_date = forms.DateField(
        label="Fecha de Nacimiento",
        help_text="Fecha de nacimiento (YYYY/MM/DD) (opcional)",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )
    phone = forms.CharField(
        max_length=20,
        label="Teléfono",
        help_text="Número de teléfono (opcional)",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1234567890'}),
    )

    # Campos User
    email = forms.EmailField(
        label="Email",
        help_text="Correo electrónico (único)",
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'usuario@example.com'}),
    )
    password = forms.CharField(
        label="Contraseña",
        help_text="Contraseña para el usuario ADMIN",
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    # Campos Admin
    department = forms.CharField(
        max_length=100,
        label="Departamento",
        help_text="Departamento del Administrador (opcional)",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Recursos Humanos'}),
    )
    hire_date = forms.DateField(
        label="Fecha de Incorporación",
        help_text="Fecha de incorporación (YYYY/MM/DD)",
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )

    # Extra
    send_welcome_email = forms.BooleanField(
        label="Enviar email de bienvenida",
        help_text="Enviar un email de bienvenida al nuevo administrador",
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    def clean_dni(self):
        """Valida formato y unicidad del DNI."""
        dni = self.cleaned_data.get("dni").strip()

        if not dni:
            raise forms.ValidationError("El DNI es requerido.")

        # Formato: 7 u 8 dígitos numéricos
        if not re.match(r'^\d{7,8}', dni):
            raise forms.ValidationError("DNI inválido. Debe tener 7 u 8 dígitos.")

        # Unicidad (delegada al service)
        if not AdminService.validate_dni_unique(dni):
            raise forms.ValidationError("El DNI ya está registrado.")

        return dni

    def clean_email(self):
        """Valida formato y unicidad del email."""
        email = self.cleaned_data.get("email").strip()

        if not email:
            raise forms.ValidationError("El email es requerido.")

        # Validar formato de email (Django lo hace automáticamente, pero reforzamos)
        try:
            validate_email(email)
        except DjangoValidationError:
            raise forms.ValidationError("Formato de email inválido.")

        # Unicidad (delegada al service)
        if not AdminService.validate_email_unique(email):
            raise forms.ValidationError("El email ya está registrado.")

        return email

    def clean_phone(self):
        """Valida formato del teléfono si se proporciona."""
        phone = self.cleaned_data.get("phone", "").strip()

        if phone and not re.match(r'^\d{7,15}$', phone):
            raise forms.ValidationError("Teléfono inválido.")

        return phone

    def clean_hire_date(self):
        """Validación básica de tipo de dato"""
        hire_date = self.cleaned_data.get("hire_date")

        if not hire_date:
            raise forms.ValidationError("La fecha de incorporación es requerida.")

        return hire_date

    def save(self):
        """Delega la creación al AdminService."""
        return AdminService.create_admin_user(self.cleaned_data)
