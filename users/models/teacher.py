from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .person import Person
from .user import User


class Teacher(Person):
    ACADEMIC_DEGREE_CHOICES = [
        ("GRADUATE", "Licenciado"),
        ("ENGINEER", "Ingeniero"),
        ("MASTER", "Magíster"),
        ("DOCTOR", "Doctor"),
        ("TEACHER", "Profesor")
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
        verbose_name="Usuario",
        help_text="Usuario del docente.",
    )

    academic_degree = models.CharField(
        choices=ACADEMIC_DEGREE_CHOICES,
        default="TEACHER",
        max_length=10,
        verbose_name="Título académico",
        help_text="Título profesional del docente."
    )

    hire_date = models.DateField(
        verbose_name="Fecha de contratación",
        help_text="Fecha de contratación del docente."
    )

    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"
        ordering = ["-hire_date"]

    def get_subjects(self):
        return self.subjects.all()

    def subject_count(self):
        return self.subjects.count()

    def __str__(self):
        degree_abbrev = {
            "GRADUATE": "Lic.",
            "ENGINEER": "Ing.",
            "MASTER": "Mag.",
            "DOCTOR": "Dr.",
            "TEACHER": "Prof."
        }
        abbrev = degree_abbrev.get(self.academic_degree, "")
        return f"{abbrev} {self.get_full_name()}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        """
        Validaciones básicas de integridad de datos.
        """
        super().clean()

        # Validar que hire_date no sea futura
        if self.hire_date and self.hire_date > timezone.now().date():
            raise ValidationError({
                'hire_date': "La fecha de contratación no puede ser futura."
            })

    @property
    def user_email(self):
        return self.user.email
