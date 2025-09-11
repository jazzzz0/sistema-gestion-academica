from django.db import models

# Create your models here.
class Career(models.Model):
    name = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name="Nombre de la carrera",
        help_text="Ingrese un nombre único para la carrera."
    )
    description = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Descripción",
        help_text="Opcional: agrege una breve descripcion de la carrera"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
        help_text="Fecha en que se creó la carrera."
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si la carrera está activa."
    )
    subjects = models.ManyToManyField("subjects.Subject", related_name="careers")
    
    def __str__(self):
        return self.name
    