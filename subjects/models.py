from django.db import models
from django.db.models.functions import Lower

# Create your models here.


class Subject(models.Model):
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
        help_text="Opcional: agrege una breve descripcion de la materia",
    )

    # Este campo será reemplazado por una relación con el modelo Teacher en el futuro
    teacher = models.CharField(
        blank=True,
        null=True,
        verbose_name="Profesor",
        help_text="Opcional: ingrese el nombre del profesor de la materia",
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
