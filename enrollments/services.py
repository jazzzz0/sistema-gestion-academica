from django.core.exceptions import ValidationError
from django.db import transaction

from enrollments.models import Enrollment
from subjects.models import Subject
from users.models import User


class EnrollmentService:
    """
    Servicio para gestionar las inscripciones de estudiantes.
    """
    @transaction.atomic
    def create_enrollment(self, user: User, subject_id: int) -> Enrollment:
        # --- Obtención de datos ---
        # Obtención de estudiante asociado al usuario
        if not hasattr(user, "student_profile"):
            raise ValidationError("El usuario no es un alumno.")
        student = user.student_profile

        # Obtener la instancia de la materia con el id especificado
        try:
            subject = Subject.objects.get(pk=subject_id)

        # Excepción: Lanzar 404 si no existe
        except Subject.DoesNotExist:
            raise ValidationError("La materia especificada no existe.")

        # --- Validación de Carrera ---
        # Verificar que la materia pertenece a la carrera del estudiante
        # Excepción: Lanzar ValidationError si no pertenece
        if not student.career.subjects.filter(pk=subject_id).exists():
            raise ValidationError("Esta materia no corresponde a tu plan de estudios.")

        # --- Validación de Unicidad ---
        # Verificar si ya existe un Enrollment asociado al estudiante y la materia
        # Para el MVP no hay recursada de materias
        # Excepción: Lanzar ValidationError si ya existe
        if Enrollment.objects.filter(student=student, subject=subject).exists():
            raise ValidationError("Ya posees una inscripción histórica para esta materia.")

        # --- Validación de Cupo ---
        # Contar inscripciones activas
        current_quota_usage = Enrollment.objects.filter(subject=subject, status="activa").count()

        # Comparar con quota de Subject
        # Si es mayor o igual a quota, lanzar ValidationError
        if current_quota_usage >= subject.quota:
            raise ValidationError("El cupo de la materia está completo.")

        # --- Creación de Inscripción ---
        enrollment = Enrollment.objects.create(
            student=student,
            subject=subject,
            status="activa"
        )

        return enrollment
