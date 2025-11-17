from django import forms
from django.contrib.auth import get_user_model

from careers.models import Career
from .services import StudentService

User = get_user_model()


class StudentCreateForm(forms.Form):
    """
    Formulario combinado para crear un User con rol STUDENT
    y su registro Student asociado.
    """
    # Campos de User
    email = forms.EmailField(
        label="Correo Electrónico",
        max_length=254,
        help_text="Ingrese un correo electrónico válido.",
    )

    # Campos de Person/Student (obligatorios)
    dni = forms.CharField(
        label="DNI",
        max_length=10,
        help_text="Documento Nacional de Identidad (7 u 8 dígitos).",
    )
    name = forms.CharField(
        label="Nombre",
        max_length=100,
        help_text="Nombre del estudiante.",
    )
    surname = forms.CharField(
        label="Apellido",
        max_length=100,
        help_text="Apellido del estudiante.",
    )
    career = forms.ModelChoiceField(
        queryset=Career.objects.all(),
        label="Carrera",
        help_text="Seleccione la carrera del estudiante.",
    )

    # Campos de Person/Student (opcionales)
    address = forms.CharField(
        label="Domicilio",
        max_length=200,
        required=False,
        help_text="Domicilio del estudiante (opcional).",
    )
    birth_date = forms.DateField(
        label="Fecha de Nacimiento",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        help_text="Fecha de nacimiento (opcional). Formato: YYYY-MM-DD.",
    )
    phone = forms.CharField(
        label="Teléfono",
        max_length=20,
        required=False,
        help_text="Número de teléfono (opcional).",
    )

    def clean_dni(self):
        """
        Valida que el DNI sea numérico y tenga entre 7 y 8 dígitos.
        """
        dni = self.cleaned_data["dni"]
        if not dni.isdigit() or not (7 <= len(dni) <= 8):
            raise forms.ValidationError("DNI inválido. Debe tener 7 u 8 dígitos numéricos.")
        return dni

    def clean_email(self):
        """
        Valida que el email no esté ya registrado.
        """
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo electrónico ya está registrado.")
        return email

    def save(self):
        data = self.cleaned_data
        return StudentService.create_user_and_student(data)
