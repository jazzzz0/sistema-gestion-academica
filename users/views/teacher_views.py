from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from users.mixins import AdminRequiredMixin
from users.forms.teacher_forms import TeacherCreateForm
from users.services.teacher_service import TeacherService


class TeacherCreateView(AdminRequiredMixin, FormView):
    template_name = "users/teachers/teacher_create.html"
    form_class = TeacherCreateForm
    success_url = reverse_lazy("dashboard")  # temporal

    def form_valid(self, form):
        try:
            teacher = TeacherService.create_teacher(form.cleaned_data)

            messages.success(
                self.request,
                f"El profesor {teacher.first_name} {teacher.last_name} "
                f"ha sido registrado correctamente con DNI {teacher.dni}."
            )

            return super().form_valid(form)

        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)
