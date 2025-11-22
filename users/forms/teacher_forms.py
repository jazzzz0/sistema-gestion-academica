from django import forms
from django.contrib.auth import get_user_model

from users.models.teacher import Teacher
from users.services.teacher_service import TeacherService

User = get_user_model()


class TeacherCreateForm(forms.Form):
    """
    Formulario combinado para crear un User con rol TEACHER
    y su registro Teacher asociado.
    """
    # Campos de User
    email = forms.EmailField(
        label="Correo Electrónico",
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'profesor@example.com'}),
        help_text="Ingrese un correo electrónico válido."
    )

    # Campos de Person (Obligatorios)
    dni = forms.CharField(
        label="DNI",
        max_length=8,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 12345678'}),
        help_text="Ingrese un DNI válido. (7 u 8 dígitos)"
    )
    name = forms.CharField(
        label="Nombre",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Juan"}),
        help_text="Nombre del profesor."
    )
    surname = forms.CharField(
        label="Apellido",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Perez"}),
        help_text="Apellido del profesor."
    )

    # Campos específicos de Teacher
    academic_degree = forms.ChoiceField(
        label="Título Académico",
        choices=Teacher.ACADEMIC_DEGREE_CHOICES,
        required=True,
        widget=forms.Select(attrs={"class": "form-select"}),
        help_text="Titulo Académico del profesor."
    )
    hire_date = forms.DateField(
        label="Fecha de Contratación",
        required=True,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        help_text="Fecha de alta en la institución."
    )

    # Campos de Person (Opcionales)
    address = forms.CharField(
        label="Domicilio",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Calle X, #Y"}),
        help_text="Domicilio del profesor."
    )
    birth_date = forms.DateField(
        label="Fecha de Nacimiento",
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        help_text="Fecha de nacimiento (YYYY/MM/DD)."
    )
    phone = forms.CharField(
        label="Teléfono",
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. 1123456789"}),
        help_text="Número de teléfono del profesor."
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
        if not self.is_valid():
            return None

        data = self.cleaned_data
        try:
            teacher = TeacherService.create_teacher_user(data)
            return teacher

        except Exception as e:
            self.add_error(None, f"Error al crear el profesor: {str(e)}")
            return None
