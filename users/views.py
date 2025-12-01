from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import AdminCreateForm, TeacherCreateForm, FirstLoginPasswordChangeForm
from .mixins import SuperuserRequiredMixin, AdminRequiredMixin
from .models import Admin, Teacher
from .services.auth_service import AuthService
from .services import AdminService
from .services.teacher_service import TeacherService


# Vista Home (para usuarios no autenticados)
class HomeView(TemplateView):
    template_name = "home.html"

    def dispatch(self, request, *args, **kwargs):
        # Si ya está autenticado, redirigimos a Dashboard
        if request.user.is_authenticated:
            return redirect('dashboard')

        # Si es anónimo, continúa con la vista Home
        return super().dispatch(request, *args, **kwargs)


# Vista Dashboard (para usuarios autenticados)
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    login_url = '/login/'
    redirect_field_name = 'next'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"
    login_url = '/login/'
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
        # Obtenemos datos del formulario
        data = form.cleaned_data
        try:
            # Llamar al servicio para crear el Admin
            admin_user = AdminService.create_admin(data)
            messages.success(
                self.request,
                f"Administrador {admin_user.surname}, {admin_user.name} creado correctamente."
                )
            return HttpResponseRedirect(self.get_success_url())
        except Exception as e:
            form.add_error(None, f"Error al crear administrador: {str(e)}")
            return self.form_invalid(form)


class AdminDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Admin
    template_name = "users/admin_confirm_delete.html"
    success_url = reverse_lazy("users:admin_list")
    context_object_name = "admin"

    # Lógica de "Borrado" suave (Override delete o form_valid)
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        admin_obj: Admin = self.object

        # Seguridad (Anti-Lockout)
        # Validamos que no se esté borrando el usuario actual
        if admin_obj.user == request.user:
            messages.error(self.request, "No puedes desactivar tu propio usuario.")
            return HttpResponseRedirect(self.get_success_url())

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


class TeacherCreateView(AdminRequiredMixin, FormView):
    form_class = TeacherCreateForm
    template_name = "users/teacher_create.html"
    success_url = reverse_lazy("users:teacher_list")

    def form_valid(self, form):
        data = form.cleaned_data
        try:
            teacher = TeacherService.create_teacher(data)
            messages.success(self.request, f"Profesor {teacher.surname}, {teacher.name} creado correctamente.")
            return HttpResponseRedirect(self.get_success_url())
        except Exception as e:
            form.add_error(None, f"Error al crear profesor: {str(e)}")
            return self.form_invalid(form)


class TeacherListView(AdminRequiredMixin, ListView):
    model = Teacher
    template_name = "users/teacher_list.html"
    context_object_name = "teachers"
    paginate_by = 20

    def get_queryset(self):
        # Optimizamos la consulta para traer los datos del Usuario relacionado
        # en el mismo viaje a la base de datos (evita N+1 queries).
        return Teacher.objects.select_related('user').all().order_by('surname', 'name')


class TeacherDeleteView(AdminRequiredMixin, DeleteView):
    """
    Vista para desactivar un profesor.
    """
    model = Teacher
    template_name = "users/teacher_confirm_delete.html"
    context_object_name = "teacher"
    success_url = reverse_lazy("users:teacher_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.object
        # Consultar las materias asignadas al profesor
        context["assigned_subjects"] = teacher.subjects.all()
        return context

    # Lógica de "Borrado" suave
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        teacher_obj: Teacher = self.object
        try:
            TeacherService.deactivate_teacher(teacher_obj)
            messages.success(
                request,
                f"El profesor {teacher_obj.surname}, {teacher_obj.name} ha sido desactivado correctamente."
            )
        except Exception as e:
            messages.error(request, f"Error al desactivar el profesor: {str(e)}")
            return HttpResponseRedirect(self.get_success_url())
        return HttpResponseRedirect(self.get_success_url())


class FirstLoginChangePasswordView(PasswordChangeView):
    template_name = "users/first_login_change_password.html"
    form_class = FirstLoginPasswordChangeForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        try:
            # Delegamos la lógica transaccional al servicio
            user = AuthService.complete_first_login_process(self.request.user, form)
            # Actualizar la sesión del usuario para que no se desloguee al cambiar el hash de la contraseña
            update_session_auth_hash(self.request, user)
            messages.success(self.request, "Contraseña cambiada correctamente.")
            # Redirigir manualmente
            return redirect(self.get_success_url())
        except Exception as e:
            messages.error(self.request, f"Ocurrió un error al actualizar la contraseña: {str(e)}")
            return self.form_invalid(form)


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    Vista para que un usuario logueado cambie su contraseña voluntariamente.
    """
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        # Agregamos un mensaje de éxito para mejorar la UX
        messages.success(self.request, "Tu contraseña ha sido actualizada correctamente.")
        return super().form_valid(form)
