from django import forms
from django.contrib.auth import get_user_model
from careers.models import Career
from .services import StudentService
from .models import Student

User = get_user_model()


class StudentForm(forms.Form):
    """
    Formulario único para crear o actualizar un estudiante + User.
    Se adapta según si recibe o no un student existente.
    """

    # === Campos de User ===
    email = forms.EmailField(
        label="Correo Electrónico",
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'nombre@ejemplo.com'})
    )

    # === Campos de Student/Person ===
    dni = forms.CharField(
        label="DNI",
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        label="Nombre",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    surname = forms.CharField(
        label="Apellido",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        label="Domicilio",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    birth_date = forms.DateField(
        label="Fecha de Nacimiento",
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    phone = forms.CharField(
        label="Teléfono",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, student: Student = None, **kwargs):
        """
        Se usa SOLO para excluir el ID actual en validaciones de unicidad
        y para pre-cargar datos iniciales.
        """
        super().__init__(*args, **kwargs)
        self.student = student

        if student:
            # Pre-cargar datos
            self.initial["email"] = student.user.email
            self.initial["dni"] = student.dni
            self.initial["name"] = student.name
            self.initial["surname"] = student.surname
            self.initial["address"] = student.address
            self.initial["birth_date"] = student.birth_date
            self.initial["phone"] = student.phone

    # === Validaciones ===
    def clean_email(self):
        email = self.cleaned_data["email"]
        qs = User.objects.filter(email=email)

        if self.student:
            qs = qs.exclude(id=self.student.user.id)

        if qs.exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean_dni(self):
        dni = self.cleaned_data["dni"].strip()
        if not dni.isdigit() or not (7 <= len(dni) <= 8):
            raise forms.ValidationError("El DNI debe tener 7 u 8 dígitos numéricos.")

        qs = Student.objects.filter(dni=dni)
        if self.student:
            qs = qs.exclude(id=self.student.id)

        if qs.exists():
            raise forms.ValidationError("Este DNI ya está registrado.")

        return dni


class StudentCareerForm(forms.ModelForm):
    career = forms.ModelChoiceField(
        queryset=Career.objects.filter(is_active=True),
        label="Carrera",
        required=False,
        empty_label="----------",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Student
        fields = ['career']
