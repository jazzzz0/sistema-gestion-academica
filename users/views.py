from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages

from users.models import Admin
from users.forms import AdminCreateForm


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


class AdminCreateView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = AdminCreateForm
    template_name = "users/admin_create.html"
    success_url = reverse_lazy("users:admin_list")

    def test_func(self):
        return self.request.user.is_superuser  # Solo superusuarios pueden acceder

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para realizar esta acción.")
        return super().handle_no_permission()

    def form_valid(self, form):
        form.save()  # Calls AdminService.create_admin_user()
        messages.success(self.request, "Administrador creado correctamente.")
        return super().form_valid(form)
