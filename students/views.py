from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.shortcuts import render, get_object_or_404, redirect
from students.forms import StudentCreateForm
from users.mixins import AdminRequiredMixin
from .models import Student
from .forms import StudentUpdateForm

class StudentCreateView(AdminRequiredMixin, FormView):
    form_class = StudentCreateForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:student-list')

    def form_valid(self, form: StudentCreateForm) -> HttpResponse:
        # El formulario se encarga de validar y guardar el estudiante
        student = form.save()

        if student:
            messages.success(self.request, f'Estudiante {student.full_name} creado correctamente.')
            return HttpResponseRedirect(self.get_success_url())
        else:
            # El guardado falló
            # El formulario ya tiene el error
            # Simplemente volvemos a mostrar el formulario
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Estudiante'
        context['action'] = 'Crear'
        return context

class StudentUpdateView(AdminRequiredMixin, FormView):
    form_class = StudentUpdateForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:student-list')

    def dispatch(self, request, *args, **kwargs):
        # Obtenemos el student que se va a editar
        self.student = get_object_or_404(Student, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """
        Pasamos el 'student' al formulario para precargar valores.
        """
        kwargs = super().get_form_kwargs()
        kwargs["student"] = self.student
        return kwargs

    def form_valid(self, form: StudentUpdateForm) -> HttpResponse:
        # El formulario se encarga de validar y actualizar
        updated_student = form.save()

        messages.success(
            self.request,
            f"Estudiante {updated_student.full_name} actualizado correctamente."
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar Estudiante"
        context["action"] = "Guardar Cambios"
        return context
       
