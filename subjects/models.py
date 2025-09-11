from django.db import models
from django.db.models.functions import Lower
# Create your models here.

class Subject(models.Model):
    name = models.CharField(
        max_length=100, 
        unique=True
    )
    description = models.TextField()
    quota = models.PositiveBigIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('name'),
                name='uq_subject_name_lower'
            )
        ]
        ordering = ['name']
        
    def __str__(self):
        return self.name
