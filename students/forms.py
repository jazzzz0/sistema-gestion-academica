from django import forms
from .services import StudentService

class StudentCreateForm(forms.Form):
    dni = forms.CharField(label="DNI", max_length=20)
    first_name = forms.CharField(label="Nombre", max_length=50)
    last_name = forms.CharField(label="Apellido", max_length=50)
    email = forms.EmailField(label="Correo electrónico")

    def clean_dni(self):
        dni = self.cleaned_data["dni"]
        if not dni.isdigit():
            raise forms.ValidationError("El DNI debe contener solo números.")
        return dni

    def save(self):
        data = self.cleaned_data
        return StudentService.create_student_and_user(data)
from django import forms
from .services import StudentService