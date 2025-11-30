from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Student

User = get_user_model()


class StudentService:
    """
    Servicio que gestiona la creación atómica de un usuario con rol STUDENT
    y su registro Student vinculado.
    """

    @staticmethod
    @transaction.atomic
    def create_student(data):
        """
        Crea un nuevo usuario (User) con rol STUDENT y el Student asociado.
        """
        # Validaciones Previas
        if not StudentService.validate_email_unique(data["email"]):
            raise ValidationError("El email ya está registrado en el sistema.")

        if not StudentService.validate_dni_unique(data["dni"]):
            raise ValidationError("El DNI ya está registrado en el sistema (puede ser Admin o Docente).")

        # Crear User con rol STUDENT
        user = User.objects.create_user(
            email=data["email"],
            role="STUDENT",
            dni=data["dni"],
        )

        # Crear Student
        student = Student.objects.create(
            user=user,
            dni=data["dni"],
            name=data["name"],
            surname=data["surname"],
            career=data.get("career"),
            address=data.get("address"),
            birth_date=data.get("birth_date"),
            phone=data.get("phone"),
        )
        return student

    @staticmethod
    @transaction.atomic
    def update_student(student: Student, *, email, dni, name, surname, career, address=None, birth_date=None,
                       phone=None):
        """
        Actualiza de manera atómica los datos del Student y su User asociado.
        """
        user = student.user

        # --- Validaciones de unicidad ---

        # Email (Excluyendo al propio usuario)
        if not StudentService.validate_email_unique(email, exclude_user_id=user.id):
            raise ValidationError({"email": "Ya existe otro usuario con este email."})

        # 2. DNI (Global + Excluyendo al propio estudiante)
        # Usamos el método robusto que chequea Admin y Teacher también.
        if not StudentService.validate_dni_unique(dni, exclude_student_id=student.id):
            raise ValidationError(
                {"dni": "El DNI ya está registrado en el sistema (puede ser otro Alumno, Admin o Docente)."})

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

        # Si el modelo User tuviera DNI, se actualizaría aquí.
        if hasattr(user, "dni"):
            user.dni = dni

        user.full_clean()
        user.save()

        return student

    @staticmethod
    @transaction.atomic
    def toggle_active_status(student_id: int, is_active: bool):
        """
        Activa o desactiva la cuenta del Student a través de su User.
        """
        student = Student.objects.select_related("user").get(pk=student_id)
        user = student.user
        user.is_active = is_active
        user.save(update_fields=["is_active"])
        return user

    # === MÉTODOS DE VALIDACIÓN ===

    @staticmethod
    def validate_dni_unique(dni: str, exclude_student_id: int = None) -> bool:
        """
        Valida que el DNI sea único en el sistema (Student, Teacher, Admin).
        Retorna True si es válido (no existe), False si ya existe.
        """
        # Importaciones locales para evitar Circular Import Error
        from users.models import Admin, Teacher

        # Verificar colisión con otros roles
        if Admin.objects.filter(dni=dni).exists():
            return False
        if Teacher.objects.filter(dni=dni).exists():
            return False

        # Verificar colisión con Students
        qs = Student.objects.filter(dni=dni)

        if exclude_student_id:
            # Si estamos editando, exclúyeme a mí mismo
            qs = qs.exclude(pk=exclude_student_id)

        if qs.exists():
            return False

        return True

    @staticmethod
    def validate_email_unique(email: str, exclude_user_id: int = None) -> bool:
        """
        Valida unicidad del email en la tabla User.
        """
        qs = User.objects.filter(email=email)

        if exclude_user_id:
            qs = qs.exclude(id=exclude_user_id)

        return not qs.exists()
