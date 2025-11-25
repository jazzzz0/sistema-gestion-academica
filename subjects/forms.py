from django import forms

from subjects.models import Subject


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "teacher", "quota", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej. Introducción a la programación",
                }
            ),
            "teacher": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "quota": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej. 30",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "3",
                    "placeholder": "Opcional: agregue una breve descripción de la materia",
                }
            ),
        }

    def clean_name(self):
        """
        Valida que el nombre sea único, transformando el "name" que se pasa
        """
        name = self.cleaned_data.get("name")

        if name:
            # 1. Transformación: Convertimos a Title Case
            # .strip() elimina espacios accidentales al inicio o final
            name = name.strip().title()

            # 2. Validación: Verificamos que no exista un registro con el mismo nombre
            # Excluimos la propia instancia (self.instance.pk) por si estamos editando.
            if Subject.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(
                    f"Ya existe una materia con el nombre '{name}'."
                )

        # 3. Retorno: Retornamos el nombre transformado
        return name



