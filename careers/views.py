from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from users.mixins import AdminRequiredMixin
from .forms import CareerForm, CareerSubjectsForm
from .models import Career


class CareerCreateView(AdminRequiredMixin, CreateView):
    """
    Vista para crear una nueva Carrera.
    Solo accesible por administradores.
    """
    model = Career
    form_class = CareerForm
    template_name = "careers/career_form.html"
    success_url = reverse_lazy("careers:career_list")

    def get_context_data(self, **kwargs):
        """Añade contexto extra para el template."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear Nueva Carrera"
        context["action"] = "Guardar"
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)

        # Forzar is_active = False.
        # 1. La Carrera se crea sin Materias, por lo tanto, debe estar inactiva.
        # 2. Se cargan las materias en un formulario independiente. (SGA-101)
        # 3. La carrera se activa.
        self.object.is_active = False
        self.object.save()

        messages.success(
            self.request,
            f"Carrera '{self.object.name}' creada en modo Borrador. "
            f"Recuerde agregar materias y activarla para que sea visible."
        )
        return redirect(self.get_success_url())

class CareerSubjectsUpdateView(AdminRequiredMixin, UpdateView):
    """
    Vista para asignar materias a una carrera. 
    Solo accesible por administradores.
    """
    
    model = Career
    form_class = CareerSubjectsForm
    template_name = "careers/career_subjects_form.html"
    context_object_name = "career"
    # No modificar name/description/is_active porque el form incluye solo 'subjects'

    def get_success_url(self):
        return reverse("career_detail", kwargs={"pk": self.object.pk})