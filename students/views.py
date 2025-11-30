from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.object

        # Buscamos las inscripciones ordenadas
        enrollments_qs = student.enrollments.all().order_by('-enrolled_at')

        # Paginamos (20 por página)
        paginator = Paginator(enrollments_qs, 20)

        # Obtenemos la página actual del request
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Enviamos 'enrollments_page' al template
        context['enrollments_page'] = page_obj
        context['page_obj'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()

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
        context["title"] = f"Actualizar Carrera del Estudiante {self.object.get_full_name()}"

        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Carrera actualizada correctamente para {self.object.get_full_name()}."
        )
        return response


class StudentToggleActiveView(AdminRequiredMixin, View):
    """
    Vista para alternar el estado (Activo/Inactivo) de un alumno.
    Delega la lógica transaccional al StudentService.
    """

    def post(self, request, pk):
        # 1. Obtener el estudiante (necesario para saber su estado actual)
        # Usamos select_related para no hacer dos queries, ya que necesitamos el user.
        student = get_object_or_404(Student.objects.select_related('user'), pk=pk)

        # 2. Calcular el nuevo estado deseado (Invertir el actual)
        # Si está activo (True) -> queremos False.
        new_status = not student.user.is_active

        try:
            # 3. Llamar a tu servicio existente
            user_updated = StudentService.toggle_active_status(student.pk, new_status)

            # 4. Feedback al usuario
            estado_texto = "reactivado" if user_updated.is_active else "dado de baja"
            messages.success(request, f"El acceso del alumno ha sido {estado_texto} correctamente.")

        except Exception as e:
            # Capturamos cualquier error inesperado del servicio
            messages.error(request, f"Ocurrió un error al intentar cambiar el estado: {str(e)}")

        # 5. Volver al perfil
        return redirect("students:student_detail", pk=pk)
