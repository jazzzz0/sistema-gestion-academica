
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import DeleteView
from users.mixins import AdminRequiredMixin
from users.models import Teacher


class TeacherDeleteView(AdminRequiredMixin, DeleteView):
    """
    Vista para desactivar un profesor (SGA-102).
    Solo accesible por Administradores.
    """
    model = Teacher
    template_name = "users/teachers/teacher_confirm_delete.html"
    context_object_name = "object"
    success_url = reverse_lazy("users:teacher_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.object

        # Consultar las materias asignadas a este profesor
        assigned_subjects = teacher.subject_set.all()  # O el related_name correspondiente si no es "subject_set"
        context["assigned_subjects"] = assigned_subjects
        return context

    def form_valid(self, form):
        teacher = self.object
        
        # Desactivar al profesor
        teacher.user.is_active = False
        teacher.user.save()

        # Si el perfil tiene is_active, también lo desactivamos
        if hasattr(teacher, 'is_active'):
            teacher.is_active = False
            teacher.save()

        # Mostrar mensaje de éxito
        messages.success(self.request, f"El profesor {teacher.first_name} {teacher.last_name} ha sido desactivado.")
        return redirect(self.success_url)

# botón para desactivar profesor en la plantilla (por ejemplo, teacher_list.html)
#<a href="{% url 'users:teacher_delete' teacher.pk %}" class="btn btn-danger">
#    Desactivar
#</a>
