from django.db import transaction

from users.models.teacher import Teacher
from users.models import User


class TeacherService:
    """
    Servicio para manejar la lógica de negocio de Profesores.
    """

    @staticmethod
    @transaction.atomic
    def create_teacher_user(data: dict) -> Teacher:
        """
        Crea un User (con rol Teacher) y un Teacher (Person)
        en una transacción atómica.

        La contraseña inicial será el DNI.
        """
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
