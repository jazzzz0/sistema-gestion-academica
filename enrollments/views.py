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
        student = self.request.user.student

        return (
            Enrollment.objects.filter(
                student=student,
                status__in=["ACTIVE", "REGULAR"]   # ajustado a tus valores reales
            )
            .select_related("subject")
            .order_by("subject__name")
        )
class EnrollmentDropView(LoginRequiredMixin, View):

    def post(self, request, pk):
        student = request.user.student

        try:
            EnrollmentService.unenroll_student(student, pk)
            messages.success(request, "Te has dado de baja correctamente.")
        except Exception as e:
            messages.error(request, str(e))

        return redirect("enrollments:my_enrollments")

    def get(self, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])
