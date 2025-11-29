from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.forms import ValidationError
from django.shortcuts import redirect
from django.views.generic import ListView, View
from django.db.models import Count, Q

from enrollments.services import EnrollmentService
from .forms import EnrollmentCreateForm

from subjects.models import Subject
from students.models import Student


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