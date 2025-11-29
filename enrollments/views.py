from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from students.models import Student
from enrollments.models import Enrollment
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse 
from django.http import HttpResponseNotAllowed
from .services import EnrollmentService
from careers.models import Career
from subjects.models import Subject
from django.db.models import Q


def inicio(request):
    return render(request, "enrollments/index.html")

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
class EnrollmentAdminListView(LoginRequiredMixin, ListView):
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

        # Para mantener los filtros en el formulario
        context["filters"] = {
            "career_id": self.request.GET.get("career_id", ""),
            "subject_id": self.request.GET.get("subject_id", ""),
            "student_dni": self.request.GET.get("student_dni", ""),
            "status": self.request.GET.get("status", ""),
        }

        return context