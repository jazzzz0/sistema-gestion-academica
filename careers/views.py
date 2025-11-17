from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from careers.forms import CareerForm
from careers.models import Career


# TODO: Necesitamos un AdminRequiredMixin para que esta vista solo pueda ser utilizada por los admins
# Ya está hecha en el ticket SGA-61
class CareerCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para crear una nueva Carrera.
    Solo accesible por administradores.
    """
    model = Career
    form_class = CareerForm
    template_name = "careers/career_form.html"

    # URL a la que redirigir después de una creación exitosa.
    success_url = reverse_lazy("careers:career_list")

    def get_context_data(self, **kwargs):
        """Añade contexto extra para el template."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear Nueva Carrera"
        context["submit_button_text"] = "Guardar"
        return context

    def form_valid(self, form):
        """
        Se llama si el formulario es válido.
        Añadimos un mensaje de éxito.
        """
        # El formulario ya guarda la instancia por defecto.
        # Guardamos la respuesta (el objeto HttpResponseRedirect)
        response = super().form_valid(form)

        # self.object es la instancia de Career que se acaba de crear
        messages.success(
            self.request,
            f"La carrera '{self.object.name}' se ha creado exitosamente."
        )
        return response