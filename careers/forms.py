from django import forms
from .models import Career


class CareerForm(forms.ModelForm):
    class Meta:
        model = Career
        # Las materias se elegirán desde la vista de edición (Update)
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: Ingeniería en Sistemas"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Opcional: Agregue una descripción de la carrera",
                }
            ),
        }

    def clean_name(self):
        """Valida que el nombre sea único (case-insensitive)."""
        name = self.cleaned_data.get("name")

        # Excluimos la propia instancia si estamos editando (para el futuro UpdateView)
        if name:
            if Career.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Ya existe una carrera con ese nombre.")

        return name
