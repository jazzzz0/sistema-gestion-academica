import re

from django.core.exceptions import ValidationError
from django.db import models


def validate_semester(value):
    if not re.match(r"^\d{4}-([12])$", value):
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
    ]

    student = models.ForeignKey("students.Student", on_delete=models.CASCADE)
    subject = models.ForeignKey("subjects.Subject", on_delete=models.CASCADE)
    semester = models.CharField(max_length=6, validators=[validate_semester])
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="activa")
    grade = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "subject"],
                name="unique_enrollment",
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.status})"

    def clean(self):
        # Validación extra de seguridad (la vista ya filtra materias válidas)
        if self.subject not in self.student.career.subjects.all():
            raise ValidationError(
                "La materia no pertenece a la carrera del estudiante."
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # ejecuta clean_fields, clean y validate_unique
        super().save(*args, **kwargs)
