from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from users.models import User
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
        # Crear User con rol STUDENT
        user = User.objects.create_user(
            email=data["email"],
            role="STUDENT",
            dni=data["dni"],
        )

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
    @staticmethod
    @transaction.atomic
    def toggle_active_status(student_id: int, is_active: bool):
        """
        Activa o desactiva la cuenta del Student a través de su User.

        Args:
            student_id (int): ID del estudiante.
            is_active (bool): Nuevo estado para el usuario.
        """
        student = Student.objects.select_related("user").get(pk=student_id)

        user = student.user
        user.is_active = is_active
        user.save(update_fields=["is_active"])

        return user

    @staticmethod
    @transaction.atomic
    def update_student_and_user(student: Student, *, email, dni, name, surname, career, address=None, birth_date=None, phone=None):
        """
        Actualiza de manera atómica los datos del Student y su User asociado.
        """

        user = student.user

        # --- Validaciones de unicidad ---
        # Email
        if User.objects.exclude(id=user.id).filter(email=email).exists():
            raise ValidationError({"email": "Ya existe un usuario con este email."})

        # DNI
        if Student.objects.exclude(id=student.id).filter(dni=dni).exists():
            raise ValidationError({"dni": "Ya existe otro estudiante con este DNI."})

        # --- Actualizar datos del STUDENT ---
        student.dni = dni
        student.name = name
        student.surname = surname
        student.career = career
        student.address = address
        student.birth_date = birth_date
        student.phone = phone
        student.full_clean()
        student.save()

        # --- Actualizar datos del USER ---
        user.email = email
        user.full_clean()
        user.save()


        return student
    
