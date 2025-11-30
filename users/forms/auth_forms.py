from django.contrib.auth.forms import PasswordChangeForm


class FirstLoginPasswordChangeForm(PasswordChangeForm):
    """
    Formulario para el cambio de contraseña obligatorio.
    Hereda de PasswordChangeForm para manejar la validación de seguridad de Django.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Aplicamos estilos
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control",
                "placeholder": field.label
            })
