from django.core.exceptions import ValidationError
from django.db import models


class Enrollment(models.Model):
    status_choices = [
        ("activa", "Activa"),
        ("regular", "Regular"),
        ("aprobada", "Aprobada"),
        ("reprobada", "Reprobada"),
        ("ausente", "Ausente"),
    ]

    student = models.ForeignKey("students.Student", on_delete=models.CASCADE)

    subject = models.ForeignKey("subjects.Subject", on_delete=models.CASCADE)

    enrolled_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=10, choices=status_choices, default="activa")

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

    # Impedir inscripciones en materias que no pertenezcan a la carrera del estudiante
    # NOTA: Esto actúa solamente como una medida extra de seguridad,
    # ya que el formulario de inscripción filtrará según las materias disponibles.
    def clean(self):
        if self.subject not in self.student.career.subjects.all():
            raise ValidationError(
                "La materia no pertenece a la carrera del estudiante."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
