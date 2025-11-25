from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView

from users.models import Admin


# Vista Home (para usuarios no autenticados)
class HomeView(TemplateView):
    template_name = "home.html"


# Vista Dashboard (para usuarios autenticados)
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    login_url = '/login/'  # Redirige a login si no está autenticado
    redirect_field_name = 'next'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"
    login_url = '/login/'  # Redirige a login si no está autenticado
    redirect_field_name = 'next'


class AdminListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Admin
    template_name = "users/admin_list.html"
    context_object_name = "admins"
    queryset = Admin.objects.select_related('user').all().order_by('-hire_date')

    def test_func(self):
        return self.request.user.is_superuser  # Solo superusuarios pueden acceder
