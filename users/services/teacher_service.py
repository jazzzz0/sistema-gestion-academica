from django.db import transaction

from users.models.teacher import Teacher
from users.models import User


class TeacherService:
    """
    Servicio para manejar la lógica de negocio de Profesores.
    """

    @staticmethod
    @transaction.atomic
    def create_teacher(data: dict) -> Teacher:
        """
        Crea un User (con rol Teacher) y un Teacher (Person)
        en una transacción atómica.

        La contraseña inicial será el DNI.
        """
        # Validaciones
        if not TeacherService.validate_email_unique(data["email"]):
            raise ValueError("El email ya está registrado en el sistema.")

        if not TeacherService.validate_dni_unique(data["dni"]):
            raise ValueError("El DNI ya está registrado en el sistema.")

        # Crear User
        user = User.objects.create_user(
            email=data["email"],
            dni=data["dni"],
            role="TEACHER",
        )

        # Crear Teacher con el User y los datos de Person
        teacher = Teacher.objects.create(
            user=user,
            name=data["name"],
            surname=data["surname"],
            dni=data["dni"],
            academic_degree=data["academic_degree"],
            hire_date=data["hire_date"],
            address=data["address"],
            birth_date=data["birth_date"],
            phone=data["phone"],
        )

        return teacher

    @staticmethod
    def validate_dni_unique(dni: str) -> bool:
        return not Teacher.objects.filter(dni=dni).exists()

    @staticmethod
    def validate_email_unique(email: str) -> bool:
        return not User.objects.filter(email=email).exists()

    @staticmethod
    @transaction.atomic
    def deactivate_teacher(teacher: Teacher) -> None:
        """
        Desactiva (Soft Delete) el perfil del profesor y su usuario asociado.
        """
        # Desactivar Usuario de Django (Login)
        if teacher.user:
            teacher.user.is_active = False
            teacher.user.save()

        # Desactivar Perfil Teacher (si tiene el campo is_active)
        if hasattr(teacher, 'is_active'):
            teacher.is_active = False
            teacher.save()
