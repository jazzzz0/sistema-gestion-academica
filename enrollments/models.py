from django.db import models


class Enrollment(models.Model):
    status_choices = [
        ("activa", "Activa"),
        ("aprobada", "Aprobada"),
        ("reprobada", "Reprobada"),
        ("ausente", "Ausente"),
    ]

    student = models.ForeignKey("students.Student", on_delete=models.CASCADE)

    subject = models.ForeignKey("subjects.Subject", on_delete=models.CASCADE)

    enrolled_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=10, choices=status_choices, default="activa")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "subject"], name="unique_enrollment"
            )
        ]
