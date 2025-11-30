from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from users.models.teacher import Teacher


User = get_user_model()


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
        """
        # Validaciones de Negocio
        if not TeacherService.validate_email_unique(data["email"]):
            raise ValidationError("El email ya está registrado en el sistema.")

        # Validación Robusta (Revisa Admin, Student y Teacher)
        if not TeacherService.validate_dni_unique(data["dni"]):
            raise ValidationError("El DNI ya está registrado en el sistema (puede ser Alumno o Admin).")

        # Crear User
        # Pasamos DNI al manager para que lo use como password inicial
        user = User.objects.create_user(
            email=data["email"],
            dni=data["dni"],
            role="TEACHER",
        )

        # Crear Teacher
        teacher = Teacher.objects.create(
            user=user,
            name=data["name"],
            surname=data["surname"],
            dni=data["dni"],
            academic_degree=data["academic_degree"],
            hire_date=data["hire_date"],
            address=data.get("address"),
            birth_date=data.get("birth_date"),
            phone=data.get("phone"),
        )

        return teacher

    @staticmethod
    @transaction.atomic
    def deactivate_teacher(teacher: Teacher) -> None:
        """
        Desactiva (Soft Delete) el perfil del profesor y su usuario asociado.
        """
        if teacher.user:
            teacher.user.is_active = False
            teacher.user.save()

        if hasattr(teacher, 'is_active'):
            teacher.is_active = False
            teacher.save()

    # === MÉTODOS DE VALIDACIÓN ===

    @staticmethod
    def validate_dni_unique(dni: str, exclude_teacher_id: int = None) -> bool:
        """
        Valida que el DNI sea único en TODO el sistema.
        Retorna True si es válido (no existe), False si ya existe.
        """
        # Importaciones locales para evitar Circular Import Error
        from users.models import Admin
        from students.models import Student

        # Verificar colisión con otros roles
        if Admin.objects.filter(dni=dni).exists():
            return False
        if Student.objects.filter(dni=dni).exists():
            return False

        # Verificar colisión con Teachers
        qs = Teacher.objects.filter(dni=dni)

        if exclude_teacher_id:
            qs = qs.exclude(pk=exclude_teacher_id)

        if qs.exists():
            return False

        return True

    @staticmethod
    def validate_email_unique(email: str, exclude_user_id: int = None) -> bool:
        qs = User.objects.filter(email=email)
        if exclude_user_id:
            qs = qs.exclude(id=exclude_user_id)
        return not qs.exists()
