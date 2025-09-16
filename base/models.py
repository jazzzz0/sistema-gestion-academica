from django.db import models


class Person(models.Model):
    """
    Modelo base abstracto para representar personas en el sistema.
    No se crea tabla en la base de datos debido a abstract = True.
    """

    name = models.CharField(
        max_length=100,
        verbose_name="Nombre",
        help_text="Nombre de la persona"
    )

    surname = models.CharField(
        max_length=100,
        verbose_name="Apellido",
        help_text="Apellido de la persona"
    )

    dni = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="DNI",
        help_text="Documento Nacional de Identidad (único)",
    )

    address = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Domicilio",
        help_text="Domicilio"
    )
    
    birth_date=models.DateField(
        null=True,
        blank=True,
        verbose_name="Nacimiento",
        help_text="Fecha de nacimiento (YYYY/MM/DD)"
    )

    # blank=True permite que sea opcional en los formularios (permite enviar un campo vacío al validar)
    # null=True permite que sea opcional en la base de datos (campo que acepta NULL)
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Teléfono",
        help_text="Número de teléfono (opcional)",
    )

    class Meta:
        # con abstract=True se evita la creación de una tabla de Person
        abstract = True
        verbose_name = "Persona"
        verbose_name_plural = "Personas"

    def __str__(self):
        return f"{self.surname}, {self.name}"
