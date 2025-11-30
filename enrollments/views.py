from django.contrib import messages
from django.forms import ValidationError
from django.shortcuts import redirect
from django.views.generic import ListView, View
from django.db.models import Count, Q
from django.http import HttpResponseNotAllowed

from users.mixins import StudentRequiredMixin, AdminRequiredMixin

from .forms import EnrollmentCreateForm
from .models import Enrollment
from .services import EnrollmentService
from careers.models import Career
from students.models import Student
from subjects.models import Subject


class StudentEnrollmentListView(StudentRequiredMixin, ListView):
    """
    Vista para listar las materias disponibles para inscripción de un estudiante.
    Muestra las materias que pertenecen a la carrera del estudiante y en las que
    no está actualmente inscrito.
    Además, anota cada materia con la cantidad de inscripciones activas.
    """
    model = Subject
    template_name = "enrollments/enrollment_list.html"
    context_object_name = "subjects"
    paginate_by = 20

    def get_queryset(self):
        student = Student.objects.get(user=self.request.user)
        queryset = (
            Subject.objects.filter(careers=student.career)
            .exclude(enrollments__student=student)
            .annotate(
                active_enrollments_count=Count(
                    "enrollments", filter=Q(enrollments__status="activa")
                )
            )
            .order_by("name")
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = Student.objects.get(user=self.request.user)
        context["student"] = student
        context["career"] = student.career
        return context


class EnrollmentActionView(StudentRequiredMixin, View):
    """
    Vista para manejar la acción de inscripción de un estudiante en una materia.
    """
    def post(self, request, *args, **kwargs):
        form = EnrollmentCreateForm(request.POST)

        if not form.is_valid():
            messages.error(request, "Datos inválidos.")
            return redirect("enrollments:enrollment_list")

        try:
            student = Student.objects.get(user=request.user)
            student = student.user
            subject = form.cleaned_data["subject"]
            EnrollmentService.create_enrollment(user=student, subject_id=subject.id)

        except ValidationError as e:
            messages.error(request, str(e))
            return redirect("enrollments:enrollment_list")

        messages.success(request, "Te has inscrito correctamente en la materia.")
        return redirect("enrollments:enrollment_list")


class MyEnrollmentListView(StudentRequiredMixin, ListView):
    """
    Vista para listar las inscripciones de un estudiante.
    """
    template_name = "enrollments/my_enrollments.html"
    context_object_name = "enrollments"

    def get_queryset(self):
        student = self.request.user.student_profile

        return (
            Enrollment.objects.filter(
                student=student,
                status__in=["activa", "regular"]
            )
            .select_related("subject")
            .order_by("subject__name")
        )


class EnrollmentDropView(StudentRequiredMixin, View):
    """
    Vista para manejar la acción de baja de una inscripción por parte del estudiante.
    """

    def post(self, request, pk):
        student = request.user.student_profile
        try:
            EnrollmentService.unenroll_student(student, pk)
            messages.success(request, "Te has dado de baja correctamente.")
        except Exception as e:
            messages.error(request, str(e))

        return redirect("enrollments:my_enrollments")

    def get(self, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])


class EnrollmentAdminListView(AdminRequiredMixin, ListView):
    """
    Vista para listar todas las inscripciones con filtros para el administrador.
    """
    model = Enrollment
    template_name = "enrollments/enrollment_admin_list.html"
    context_object_name = "enrollments"
    paginate_by = 20

    def get_queryset(self):
        qs = (
            Enrollment.objects.select_related(
                "student",
                "student__user",
                "subject",
                "student__career",
            )
        )

        # --- Filtros dinámicos ---
        career_id = self.request.GET.get("career_id")
        subject_id = self.request.GET.get("subject_id")
        student_dni = self.request.GET.get("student_dni")
        status = self.request.GET.get("status")

        if career_id:
            qs = qs.filter(student__career_id=career_id)

        if subject_id:
            qs = qs.filter(subject_id=subject_id)

        if student_dni:
            qs = qs.filter(student__dni=student_dni)

        if status:
            qs = qs.filter(status=status)

        return qs.order_by("-enrolled_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Para llenar los <select>
        context["careers"] = Career.objects.all().order_by("name")
        context["subjects"] = Subject.objects.all().order_by("name")

        # Para llenar el <select> de status
        context["status_choices"] = Enrollment.STATUS_CHOICES

        # Para mantener los filtros en el formulario
        context["filters"] = {
            "career_id": self.request.GET.get("career_id", ""),
            "subject_id": self.request.GET.get("subject_id", ""),
            "student_dni": self.request.GET.get("student_dni", ""),
            "status": self.request.GET.get("status", ""),
        }

        return context
