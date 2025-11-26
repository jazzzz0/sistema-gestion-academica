from django import forms

from subjects.models import Subject


class EnrollmentCreateForm(forms.Form):
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.HiddenInput,
        error_messages={
            "required": "No se especificó ninguna materia.",
            "invalid_choice": "La materia seleccionada no es válida.",
        }
    )
