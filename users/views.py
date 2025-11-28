from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from .mixins import SuperuserRequiredMixin
from .models import Admin
from .forms import AdminCreateForm


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


class AdminListView(SuperuserRequiredMixin, ListView):
    model = Admin
    template_name = "users/admin_list.html"
    context_object_name = "admins"
    queryset = Admin.objects.select_related('user').all().order_by('-hire_date')
    paginate_by = 20


class AdminCreateView(SuperuserRequiredMixin, FormView):
    form_class = AdminCreateForm
    template_name = "users/admin_create.html"
    success_url = reverse_lazy("users:admin_list")

    def form_valid(self, form):
        form.save()  # Calls AdminService.create_admin_user()
        messages.success(self.request, "Administrador creado correctamente.")
        return super().form_valid(form)


class AdminDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Admin
    template_name = "users/admin_confirm_delete.html"
    success_url = reverse_lazy("users:admin_list")
    context_object_name = "admin"

    # Lógica de "Borrado" suave (Override delete o form_valid)
    def delete(self, request, *args, **kwargs):
        # Obtenemos el objeto Admin a desactivar
        self.object = self.get_object()

        admin_obj: Admin = self.object

        # Seguridad (Anti-Lockout)
        # Validamos que no se esté borrando el usuario actual
        if admin_obj.user == request.user:
            messages.error(self.request, "No puedes desactivar tu propio usuario.")
            return HttpResponseRedirect(self.get_success_url())

        # Lógica de borrado suave
        try:
            with transaction.atomic():
                # Desactivar el perfil Admin
                admin_obj.is_active = False
                admin_obj.save()

                # Desactivar el Usuario de Django
                if admin_obj.user:
                    admin_obj.user.is_active = False
                    admin_obj.user.save()

            messages.success(request, "Administrador desactivado correctamente.")

        except Exception as e:
            messages.error(request, f"Error al desactivar el administrador: {str(e)}")

        return HttpResponseRedirect(self.get_success_url())
