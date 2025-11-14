from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView


# Vista Home (para usuarios no autenticados)
class HomeView(TemplateView):
    template_name = "home.html"


# Vista Dashboard (para usuarios autenticados)
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    login_url = 'users:login'  # Redirige a login si no está autenticado
    redirect_field_name = 'next'
