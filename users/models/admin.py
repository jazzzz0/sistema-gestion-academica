from . import Person, User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class Admin(Person):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="admin_profile",
        verbose_name="Usuario",
        help_text="Usuario asociado a este administrador",
    )

    department = models.CharField(
        blank=True,
        null=True,
        verbose_name="Departamento",
        help_text="Departamento del administrador",
    )

    hire_date = models.DateField(
        verbose_name="Fecha de incorporación",
        help_text="Fecha de incorporación del administrador",
    )


    def clean(self):
        """
        Ejecuta las validaciones del modelo antes de guardar.
        """
        errors = {}
        
        # Validar que el usuario existe
        if not self.user:
            errors['user'] = "El administrador debe tener un usuario asociado."
 
        # Validar que hire_date no sea futura
        if self.hire_date:
            if self.hire_date > timezone.now().date():
                errors['hire_date'] = "La fecha de incorporación no puede ser futura."
        
        if errors:
            raise ValidationError(errors)
    
    def _sync_user_staff_status(self):
        """
        Sincroniza el estado is_staff del usuario asociado.
        Asegura que user.is_staff = True para todos los administradores.
        """
        if self.user and not self.user.is_staff:
            self.user.is_staff = True
            self.user.save(update_fields=['is_staff'])
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para ejecutar las validaciones
        y sincronizar el estado del usuario asociado.
        """
        # Ejecutar validaciones
        self.full_clean()
        
        # Sincronizar is_staff del usuario
        self._sync_user_staff_status()
        
        # Guardar el objeto Admin
        super().save(*args, **kwargs)

    def __str__(self):
        return super().__str__()

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"
        ordering = ["-hire_date"]
        indexes = [
            models.Index(fields=["department"], name="admin_department_idx"),
        ]
        