from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from subjects.forms import SubjectForm
from subjects.models import Subject
from users.mixins import AdminRequiredMixin


class SubjectCreateView(AdminRequiredMixin, CreateView):
    """
    Vista para crear una nueva Materia.
    Solo accesible por Administradores.
    """
    model = Subject
    form_class = SubjectForm
    template_name = "subjects/subject_form.html"
    success_url = reverse_lazy("subjects:subject_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Materia'
        context['action'] = 'Crear'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Materia {form.cleaned_data["name"]} creada correctamente.'
        )
        return response


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Materia'
        context['action'] = 'Actualizar'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"La materia '{self.object.name}' ha sido actualizada correctamente."
        )
        return response
