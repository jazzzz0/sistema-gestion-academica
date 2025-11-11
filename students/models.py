from django.core.exceptions import ValidationError
from django.db import models

from users.models import Person
from careers.models import Career


class Student(Person):
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="student_profile",
        verbose_name="Usuario",
        help_text="Usuario asociado a este estudiante",
    )

    career = models.ForeignKey(
        Career,
        on_delete=models.PROTECT,  # Evita borrar una carrera si tiene estudiantes asociados
        related_name="students",
        verbose_name="Carrera",
        help_text="Carrera del estudiante",
    )

    def clean(self):
        """
        Valida que exista un User asociado a esta Persona (Student).
        """
        super().clean()

        # Verificar si existe un User asociado a esta Persona
        if not hasattr(self, "user") or self.user is None:
            raise ValidationError(
                {
                    "dni": "No existe un usuario asociado a esta persona. "
                    "Debe crear primero un usuario con rol STUDENT para esta persona."
                }
            )

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para ejecutar las validaciones.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return super().__str__() + f" ({self.career}) "

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
