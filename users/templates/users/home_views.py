from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "users/home.html"
    # Aquí iría la lógica para la vista de inicio de usuarios
