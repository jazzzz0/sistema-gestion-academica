from django import forms

from careers.models import Career


class CareerForm(forms.ModelForm):
    class Meta:
        model = Career
        # Las materias se elegirán desde la vista de edición (Update)
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Ej: Tecnicatura en Programación'}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Opcional: Agregue una descripción de la carrera",
                }
            ),
        }

    # Validación para el 'name' por buena práctica
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name and Career.objects.filter(name=name).exists():
            raise forms.ValidationError("Ya existe una carrera con ese nombre")
        return name
