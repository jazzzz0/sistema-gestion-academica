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
    career = forms.ModelChoiceField(
        queryset=Career.objects.all(),
        label="Carrera",
        widget=forms.Select(attrs={'class': 'form-select'})
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
        student (None o Student):
            - Si None → Modo creación
            - Si Student → Modo edición (precargar valores y validar distinto)
        """
        super().__init__(*args, **kwargs)
        self.student = student

        if student:
            # Precargar datos existentes para edición
            self.initial["email"] = student.user.email
            self.initial["dni"] = student.dni
            self.initial["name"] = student.name
            self.initial["surname"] = student.surname
            self.initial["career"] = student.career
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

    # === Guardado genérico ===
    def save(self):
        if not self.is_valid():
            return None

        data = self.cleaned_data

        if self.student:
            # --- Modo actualización ---
            return StudentService.update_student_and_user(
                self.student,
                email=data["email"],
                dni=data["dni"],
                name=data["name"],
                surname=data["surname"],
                career=data["career"],
                address=data.get("address"),
                birth_date=data.get("birth_date"),
                phone=data.get("phone"),
            )
        else:
            # --- Modo creación ---
            return StudentService.create_user_and_student(data)
