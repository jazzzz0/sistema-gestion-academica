from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from users.mixins import AdminRequiredMixin
from users.forms.teacher_forms import TeacherCreateForm


class TeacherCreateView(AdminRequiredMixin, FormView):
    """
    Vista para dar de alta un nuevo Profesor (User + Person).
    Usa un FormView porque el formulario maneja lógica compleja (Servicio).
    """
    template_name = "users/teacher_forms.html"  # Ruta sugerida
    form_class = TeacherCreateForm
    success_url = reverse_lazy("users:teacher-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Registrar Nuevo Profesor"
        context["action"] = "Guardar"
        return context

    def form_valid(self, form):
        # El form.save() llama al TeacherService
        teacher = form.save()

        if teacher:
            messages.success(
                self.request,
                f"El profesor {teacher.name} {teacher.surname} ha sido registrado exitosamente."
            )
            return super().form_valid(form)
        else:
            # Fallback por si save() devuelve None (aunque el form maneja errores)
            messages.error(self.request, "Ocurrió un error al intentar guardar.")
            return self.form_invalid(form)