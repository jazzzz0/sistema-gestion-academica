from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.mixins import AdminRequiredMixin
from .forms import CareerForm
from .models import Career


class CareerCreateView(AdminRequiredMixin, CreateView):
    """
    Vista para crear una nueva Carrera.
    Solo accesible por administradores.
    """
    model = Career
    form_class = CareerForm
    template_name = "careers/career_form.html"
    success_url = reverse_lazy("careers:career-list")

    def get_context_data(self, **kwargs):
        """Añade contexto extra para el template."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear Nueva Carrera"
        context["action"] = "Guardar"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"La carrera '{self.object.name}' se ha creado exitosamente."
        )
        return response
