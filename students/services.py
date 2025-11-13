from django.db import transaction
from django.contrib.auth import get_user_model
from .models import Student

User = get_user_model()

class StudentService:
    """
    Servicio que gestiona la creación atómica de un usuario con rol STUDENT
    y su registro Student vinculado.
    """

    @staticmethod
    @transaction.atomic
    def create_student_and_user(data):
        """
        Crea un nuevo usuario (User) con rol STUDENT y el Student asociado.
        data = {
            "email": ...,
            "dni": ...,
            "first_name": ...,
            "last_name": ...,
        }
        """
        # Crear el usuario
        user = User.objects.create_user(
            email=data["email"],
            dni=data["dni"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            role="STUDENT",
            password=data["dni"],  # contraseña inicial = DNI
        )

        # Crear el registro de alumno vinculado
        student = Student.objects.create(
            user=user,
            dni=data["dni"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )

        return student
