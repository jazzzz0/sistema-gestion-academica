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
    def create_user_and_student(data):
        """
        Crea un nuevo usuario (User) con rol STUDENT y el Student asociado.
        Args:
            data (dict): Diccionario con los datos necesarios para crear el usuario y el estudiante.
        Returns:
            Student: El objeto Student creado.
        """
        # Validar campos obligatorios
        required_fields = ["email", "dni", "name", "surname", "career"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Faltan campos obligatorios: {', '.join(missing_fields)}")

        # Crear User con rol STUDENT
        user = User.objects.create_user(
            email=data["email"],
            role="STUDENT",
            password=data["dni"],
        )

        # Forzar cambio de contraseña en el primer login
        user.is_first_login = True
        user.save(update_fields=["is_first_login"])

        # Crear Student (con campos de Person)
        student = Student.objects.create(
            user=user,
            dni=data["dni"],
            name=data["name"],
            surname=data["surname"],
            career=data["career"],
            address=data.get("address"),
            birth_date=data.get("birth_date"),
            phone=data.get("phone"),
        )

        return student
