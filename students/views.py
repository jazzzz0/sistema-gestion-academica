from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView, ListView, DetailView
from django.views import View
from django.db.models import Q

from users.mixins import AdminRequiredMixin
from .models import Student
from .forms import StudentForm
from students.services.student_service import StudentService


class StudentCreateView(AdminRequiredMixin, FormView):
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:student_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["student"] = None
        return kwargs

    def form_valid(self, form):
        student = form.save()
        messages.success(self.request, f"Estudiante {student.get_full_name()} creado correctamente.")
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear Estudiante"
        context["action"] = "Crear"
        return context


class StudentUpdateView(AdminRequiredMixin, FormView):
    form_class = StudentForm
    template_name = "students/student_form.html"
    success_url = reverse_lazy("students:student_list")

    def dispatch(self, request, *args, **kwargs):
        self.student = get_object_or_404(Student, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["student"] = self.student
        return kwargs

    def form_valid(self, form):
        student = form.save()
        messages.success(self.request, f"Estudiante {student.get_full_name()} actualizado correctamente.")
        return redirect("students:student_detail", pk=student.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar Estudiante"
        context["action"] = "Guardar Cambios"
        return context


class StudentListView(AdminRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 20  # Requisito de paginación por defecto

    def get_queryset(self):
        # Optimizamos la consulta trayendo los datos del usuario relacionado
        # y ordenamos por apellido/nombre para una visualización consistente
        queryset = Student.objects.select_related('user').all().order_by('surname', 'name')

        # Capturar el parámetro de búsqueda desde GET
        search_query = self.request.GET.get('search', '').strip()

        if search_query:
            # Filtrar por nombre, apellido o email (case-insensitive)
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(surname__icontains=search_query) |
                Q(user__email__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Alumnos'
        context['search_query'] = self.request.GET.get('search', '')
        return context


class StudentDetailView(AdminRequiredMixin, DetailView):
        model = Student
        template_name = "students/student_detail.html"
        context_object_name = 'student'

        def get_queryset(self):
        # Optimización para evitar N+1
            return Student.objects.select_related("user", "career")


class DeactivateStudentView(UserPassesTestMixin, View):
    def post(self, request, student_id, *args, **kwargs):
        # Check if the user has the required permissions
        if not self.test_func():
            return self.handle_no_permission()

        # Call the service to toggle the student's active status
        success = StudentService.toggle_active(student_id)

        if success:
            messages.success(request, "El estado del alumno ha sido actualizado correctamente.")
        else:
            messages.error(request, "Hubo un error al intentar actualizar el estado del alumno.")

        # Redirect back to the student detail view
        return HttpResponseRedirect(reverse('students:student_detail', args=[student_id]))

    def test_func(self):
        # Allow only superusers or users with the ADMIN role
        return self.request.user.is_superuser or self.request.user.role == 'ADMIN'

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para realizar esta acción.")
        return HttpResponseRedirect(reverse('students:student_list'))

