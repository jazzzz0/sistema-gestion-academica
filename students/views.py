from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView, ListView, DetailView, UpdateView
from django.views import View
from django.db.models import Q

from users.mixins import AdminRequiredMixin
from .forms import StudentForm, StudentCareerForm
from .models import Student
from .services import StudentService


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


class StudentUpdateView(AdminRequiredMixin, FormView):
    form_class = StudentForm
    template_name = "students/student_form.html"
    success_url = reverse_lazy("students:student_list")

    def dispatch(self, request, *args, **kwargs):
        self.student = get_object_or_404(Student, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.student
        return kwargs

    def form_valid(self, form):
        # OJO: No llamamos a form.save() aquí.
        # Extraemos los datos limpios del formulario (cleaned_data)
        data = form.cleaned_data

        try:
            # Delegamos la lógica "pesada" al servicio
            StudentService.update_student_and_user(
                student=self.student,
                email=data.get('email'),
                dni=data.get('dni'),
                name=data.get('name'),
                surname=data.get('surname'),
                career=data.get('career'),
                address=data.get('address'),
                birth_date=data.get('birth_date'),
                phone=data.get('phone')
            )
            messages.success(self.request, f"Estudiante {self.student.get_full_name()} actualizado correctamente.")
            return redirect("students:student_detail", pk=self.student.pk)

        except ValidationError as e:
            # Si el servicio lanza un error de validación (ej. email duplicado)
            # lo agregamos al formulario y volvemos a renderizar
            form.add_error(None, e)
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar Estudiante"
        context["action"] = "Guardar Cambios"
        return context


class StudentCareerUpdateView(AdminRequiredMixin, UpdateView):
    model = Student
    form_class = StudentCareerForm
    template_name = "students/student_career_form.html"

    def get_success_url(self):
        return reverse_lazy("students:student_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Verificar si el estudiante tiene inscripciones activas
        context["has_enrollments"] = self.object.enrollments.exists()
        context["title"] = f"Actualizar Carrera del Estudiante {self.object.full_name}"

        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Carrera actualizada correctamente para {self.object.full_name}."
        )
        return response


class StudentToggleActiveView(AdminRequiredMixin, View):
    """
        Vista para alternar el estado (Activo/Inactivo) de un alumno.
        Solo accesible por Admin/Superuser.
    """
    def post(self, request, pk):
        # Obtener el estudiante o 404
        student = get_object_or_404(Student, pk=pk)

        # Calcular el nuevo estado
        new_status = not student.user.is_active

        # Llamar al servicio para actualizar el estado
        StudentService.toggle_active_status(student.pk, new_status)

        # Feedback al usuario
        status_msg = "reactivado" if new_status else "dado de baja"
        messages.success(request, f"El alumno {student.surname} ha sido {status_msg} correctamente.")

        # Redirigir al detalle del alumno
        return redirect("students:student_detail", pk=pk)
