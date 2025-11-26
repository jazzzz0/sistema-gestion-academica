from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

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