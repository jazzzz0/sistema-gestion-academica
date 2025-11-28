from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from users.mixins import AdminRequiredMixin
from subjects.forms import SubjectForm
from subjects.models import Subject


class SubjectCreateView(AdminRequiredMixin, CreateView):
    """
    Vista para crear una nueva Materia.
    Solo accesible por Administradores.
    """
    model = Subject
    form_class = SubjectForm
    template_name = "subjects/subject_form.html"
    success_url = reverse_lazy("subjects:subject_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Materia {form.cleaned_data["name"]} creada correctamente.'
        )
        return response


class SubjectListView(AdminRequiredMixin, ListView):

    model = Subject
    template_name = "subjects/subject_list.html"
    context_object_name = "subjects"
    paginate_by = 20

    def get_queryset(self):
        """
        AC:
        - Todas las materias
        - Orden alfabético ascendente por nombre
        - select_related('teacher') para evitar N+1 queries
        """
        return (
            Subject.objects.all()
            .select_related("teacher")
            .order_by("name")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Gestión de Materias"
        return context


class SubjectDetailView(AdminRequiredMixin, DetailView):
    """
    Ficha técnica de la Materia (SGA-89).
    Solo accesible por Administradores.
    """
    model = Subject
    template_name = "subjects/subject_detail.html"
    context_object_name = "subject"

    def get_queryset(self):
        """
        Optimización requerida:
        - prefetch enrollments (enrollment_set o related_name)
        - prefetch careers
        """
        return (
            Subject.objects.all()
            .select_related("teacher")
            .prefetch_related("enrollment_set")        # o el related_name que usen
            .prefetch_related("careers")               # idem
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        subject = context["subject"]

        # Contar alumnos activos
        # Si usás algún filtro tipo active=True lo ajustamos después
        enrollments = subject.enrollment_set.all()
        context["enrollment_count"] = enrollments.count()

        return context


class SubjectUpdateView(AdminRequiredMixin, UpdateView):
    """
    Vista para editar una Subject existente.
    Solo accesible por Administradores.
    """
    model = Subject
    form_class = SubjectForm
    template_name = "subjects/subject_form.html"
    success_url = reverse_lazy("subjects:subject_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"La materia '{self.object.name}' ha sido actualizada correctamente."
        )
        return response


class SubjectDeleteView(AdminRequiredMixin, DeleteView):
    """
    Vista para eliminar una Subject existente.
    Solo accesible por Administradores.
    """
    model = Subject
    template_name = "subjects/subject_confirm_delete.html"
    success_url = reverse_lazy("subjects:subject_list")
    context_object_name = "subject"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = self.get_object()
        # Indica si hay inscripciones asociadas (bloqueante)
        context["has_enrollments"] = subject.enrollments.exists()
        # Lista de carreras asociadas (informativo)
        context["careers"] = subject.careers.all()
        context["title"] = "¿Eliminar Materia?"
        return context

    def delete(self, request, *args, **kwargs):
        subject = self.get_object()
        # Verificar inscripciones: si existen, no permitir borrado
        if subject.enrollments.exists():
            messages.error(
                request,
                "No se puede eliminar la materia porque tiene historial académico (alumnos inscritos)."
            )
            return redirect(self.success_url)

        # No hay inscripciones: proceder a borrar. Las relaciones M2M con carreras
        # serán limpiadas automáticamente por Django.
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "Materia eliminada correctamente.")
        return response
