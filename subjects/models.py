from django.db import models
from django.db.models.functions import Lower

from users.models.teacher import Teacher


class Subject(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        related_name="subjects",
        verbose_name="Docente",
        help_text="Docente encargado de la materia",
        null=True,
        blank=True,
    )

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre de la materia",
        help_text="Ingrese un nombre único para la materia.",
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción",
        help_text="Opcional: agregue una breve descripción de la materia",
    )

    quota = models.PositiveIntegerField(
        default=30,
        verbose_name="Cupo",
        help_text="Cantidad máxima de estudiantes permitidos en la materia",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("name"), name="uq_subject_name_lower")
        ]
        ordering = ["name"]

    def __str__(self):
        return self.name
