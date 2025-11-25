import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


def validate_semester(value):
    if not value:
        return
    if not re.match(r"^\d{4}-[12]$", value):
        raise ValidationError(
            f"{value} no es un semestre válido. Formato esperado: 'YYYY-1' o 'YYYY-2'."
        )


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ("activa", "Activa"),
        ("regular", "Regular"),
        ("aprobada", "Aprobada"),
        ("reprobada", "Reprobada"),
        ("ausente", "Ausente"),
        ("baja", "Baja"),
    ]

    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="Inscripción",
        help_text="Estudiante que realiza la inscripción.",
    )

    subject = models.ForeignKey(
        "subjects.Subject",
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="Materia",
        help_text="Materia a la que se inscribe el estudiante.",
    )

    semester = models.CharField(
        max_length=6,
        validators=[validate_semester],
        editable=False,
        verbose_name="Semestre",
        help_text="Se genera automáticamente al crear la inscripción.",
    )

    enrolled_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de inscripción",
        help_text="Fecha y hora en que se realizó la inscripción.",
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="activa",
        verbose_name="Estado",
        help_text="Estado actual de la inscripción.",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "subject"],
                name="unique_enrollment",
            )
        ]
        ordering = ["-enrolled_at", "student__surname", "subject__name"]
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"

    @staticmethod
    def get_semester_from_date(date):
        year = date.year
        semester = 1 if date.month <= 6 else 2
        return f"{year}-{semester}"

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.status})"

    def clean(self):
        # Validación extra de seguridad (la vista ya filtra materias válidas)
        if not self.student.career.subjects.filter(pk=self.subject_id).exists():
            raise ValidationError(
                "La materia no pertenece a la carrera del estudiante."
            )

    def save(self, *args, **kwargs):
        if not self.semester:
            date = self.enrolled_at or timezone.now()
            self.semester = self.get_semester_from_date(date)
        self.full_clean()  # ejecuta clean_fields, clean y validate_unique
        super().save(*args, **kwargs)
