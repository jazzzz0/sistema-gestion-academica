from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.forms import ValidationError
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, View
from django.db.models import Count, Q
from django.urls import revers
from django.http import HttpResponseNotAllowed

from enrollments.services import EnrollmentService
from .forms import EnrollmentCreateForm

from subjects.models import Subject
from students.models import Student
from enrollments.models import Enrollment


class StudentEnrollmentListView(LoginRequiredMixin, ListView):
    """
    Vista para listar las materias disponibles para inscripción de un estudiante.
    Muestra las materias que pertenecen a la carrera del estudiante y en las que
    no está actualmente inscrito.
    Además, anota cada materia con la cantidad de inscripciones activas.
    """
    model = Subject
    template_name = "enrollments/enrollment_list.html"
    context_object_name = "subjects"

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


class EnrollmentActionView(LoginRequiredMixin, View):
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
            subject = form.cleaned_data["subject"]
            EnrollmentService.create_enrollment(student=student, subject=subject)

        except ValidationError as e:
            messages.error(request, str(e))
            return redirect("enrollments:enrollment_list")
        
        messages.success(request, "Te has inscrito correctamente en la materia.")
        return redirect("enrollments:enrollment_list")

class MyEnrollmentListView(LoginRequiredMixin, ListView):
    template_name = "enrollments/my_enrollments.html"
    context_object_name = "enrollments"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == "STUDENT":
            messages.error(request, "No tienes permiso para ver tus inscripciones.")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

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
      
class EnrollmentDropView(LoginRequiredMixin, View):

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

