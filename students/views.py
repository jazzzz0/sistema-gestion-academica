from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.shortcuts import render, get_object_or_404, redirect
from students.forms import StudentCreateForm
from users.mixins import AdminRequiredMixin
from .models import Student
from .forms import StudentForm

class StudentCreateView(AdminRequiredMixin, FormView):
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:student-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["student"] = None
        return kwargs

    def form_valid(self, form):
        student = form.save()
        messages.success(self.request, f"Estudiante {student.full_name} creado correctamente.")
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Crear Estudiante"
        ctx["action"] = "Crear"
        return ctx


class StudentUpdateView(AdminRequiredMixin, FormView):
    form_class = StudentForm
    template_name = "students/student_form.html"
    success_url = reverse_lazy("students:student-list")

    def dispatch(self, request, *args, **kwargs):
        self.student = get_object_or_404(Student, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["student"] = self.student
        return kwargs

    def form_valid(self, form):
        student = form.save()
        messages.success(self.request, f"Estudiante {student.full_name} actualizado correctamente.")
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Editar Estudiante"
        ctx["action"] = "Guardar Cambios"
        return ctx
