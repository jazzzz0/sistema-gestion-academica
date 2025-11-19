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

    # --- Campos de User ---
    email = forms.EmailField(
        label="Correo Electrónico",
        max_length=254,
        help_text="Ingrese un correo electrónico válido.",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'nombre@ejemplo.com'})
    )

    # --- Campos de Person/Student (obligatorios) ---
    dni = forms.CharField(
        label="DNI",
        max_length=10,
        help_text="Documento Nacional de Identidad (7 u 8 dígitos).",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12345678'})
    )
    name = forms.CharField(
        label="Nombre",
        max_length=100,
        help_text="Nombre del estudiante.",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    surname = forms.CharField(
        label="Apellido",
        max_length=100,
        help_text="Apellido del estudiante.",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    career = forms.ModelChoiceField(
        queryset=Career.objects.all(),
        label="Carrera",
        help_text="Seleccione la carrera del estudiante.",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # --- Campos de Person/Student (opcionales) ---
    address = forms.CharField(
        label="Domicilio",
        max_length=200,
        required=False,
        help_text="Domicilio del estudiante (opcional).",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    birth_date = forms.DateField(
        label="Fecha de Nacimiento",
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        help_text="Fecha de nacimiento (opcional).",
    )
    phone = forms.CharField(
        label="Teléfono",
        max_length=20,
        required=False,
        help_text="Número de teléfono (opcional).",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def clean_dni(self):
        dni = self.cleaned_data["dni"].strip()
        if not dni.isdigit() or not (7 <= len(dni) <= 8):
            raise forms.ValidationError("DNI inválido. Debe tener 7 u 8 dígitos numéricos.")
        return dni

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo electrónico ya está registrado.")
        return email

    def save(self):
        if not self.is_valid():
            return None

        try:
            return StudentService.create_user_and_student(self.cleaned_data)
        except Exception as e:
            self.add_error(None, f"Error al crear el estudiante: {str(e)}")
            return None
