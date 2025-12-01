from django import forms
from .models import Career
from subjects.models import Subject


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


class CareerSubjectsForm(forms.ModelForm):
    class Meta:
        model = Career
        fields = ["subjects"]

        widgets = {
            "subjects": forms.SelectMultiple(
                attrs={
                    "class": "form-control select2-subjects",
                    "style": "width: 100%",
                    "data-placeholder": "Buscar materias para agregar...",
                },
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subjects"].queryset = Subject.objects.all().order_by("name")
        self.fields["subjects"].label = "Plan de Estudios"
