from django.contrib import messages
from django.db.models import Count
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from users.mixins import AdminRequiredMixin, TeacherRequiredMixin
from subjects.forms import SubjectForm
from subjects.models import Subject
from enrollments.models import Enrollment


class SubjectCreateView(AdminRequiredMixin, CreateView):
    """
    Vista para crear una nueva Materia.
    Solo accesible por Administradores.
    """
    model = Subject
    form_class = SubjectForm
    template_name = "subjects/subject_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Materia {form.cleaned_data["name"]} creada correctamente.'
        )
        return response
    
    def get_success_url(self):
        return reverse_lazy("subjects:subject_detail", kwargs={"pk": self.object.pk})


class SubjectListView(AdminRequiredMixin, ListView):

    model = Subject
    template_name = "subjects/subject_list.html"
    context_object_name = "subjects"
    paginate_by = 20

    def get_queryset(self):
        """
        AC:
        - Todas las materias
        - Orden alfabético ascendente por nombre
        - select_related('teacher') para evitar N+1 queries
        """
        return (
            Subject.objects.all()
            .select_related("teacher")
            .order_by("name")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Gestión de Materias"
        return context


class SubjectDetailView(AdminRequiredMixin, DetailView):
    """
    Ficha técnica de la Materia (SGA-89).
    Solo accesible por Administradores.
    """
    model = Subject
    template_name = "subjects/subject_detail.html"
    context_object_name = "subject"

    def get_queryset(self):
        """
        Optimización aplicada:
        1. select_related: Trae el profesor en la misma query.
        2. prefetch_related: Trae las carreras.
        3. annotate: Cuenta los enrollments directamente en la DB.
        """
        return (
            Subject.objects.all()
            .select_related("teacher")
            .prefetch_related("careers")
            .annotate(enrollment_count=Count('enrollments'))
        )


class SubjectUpdateView(AdminRequiredMixin, UpdateView):
    """
    Vista para editar una Subject existente.
    Solo accesible por Administradores.
    """
    model = Subject
    form_class = SubjectForm
    template_name = "subjects/subject_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"La materia ha sido actualizada correctamente."
        )
        return response

    def get_success_url(self):
        return reverse_lazy("subjects:subject_detail", kwargs={"pk": self.object.pk})


class SubjectDeleteView(AdminRequiredMixin, DeleteView):
    """
    Vista para eliminar una Subject existente.
    Solo accesible por Administradores.
    """
    model = Subject
    template_name = "subjects/subject_confirm_delete.html"
    success_url = reverse_lazy("subjects:subject_list")
    context_object_name = "subject"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = self.get_object()
        # Indica si hay inscripciones asociadas (bloqueante)
        context["has_enrollments"] = subject.enrollments.exists()
        # Lista de carreras asociadas (informativo)
        context["careers"] = subject.careers.all()
        context["title"] = "¿Eliminar Materia?"
        return context

    def delete(self, request, *args, **kwargs):
        subject = self.get_object()
        # Verificar inscripciones: si existen, no permitir borrado
        if subject.enrollments.exists():
            messages.error(
                request,
                "No se puede eliminar la materia porque tiene historial académico (alumnos inscritos)."
            )
            return redirect(self.get_success_url())

        # No hay inscripciones: proceder a borrar. Las relaciones M2M con carreras
        # serán limpiadas automáticamente por Django.
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "Materia eliminada correctamente.")
        return response


class MySubjectsListView(TeacherRequiredMixin, ListView):
    model = Subject
    template_name = "subjects/my_subjects.html"
    context_object_name = "subjects"

    def get_queryset(self):
        # Obtenemos el perfil del profesor del usuario logueado
        teacher = self.request.user.teacher_profile

        # Filtramos las materias donde este profesor es el titular
        return (
            Subject.objects.filter(teacher=teacher)
            .prefetch_related('careers', 'enrollments')
            .order_by('name')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Mis Materias Asignadas"
        return context


class SubjectEnrollmentListView(TeacherRequiredMixin, ListView):
    model = Enrollment
    template_name = "subjects/subject_enrollment_list.html"
    context_object_name = "enrollments"

    def get_queryset(self):
        # Capturamos el ID de la materia de la URL
        subject_id = self.kwargs['pk']

        # Obtenemos el perfil del profesor actual
        teacher = self.request.user.teacher_profile

        # Buscamos la materia, pero filtrando por el profesor.
        # Si la materia existe pero es de otro profesor, lanzará 404 Not Found.
        self.subject = get_object_or_404(Subject, pk=subject_id, teacher=teacher)

        # 4. Retornamos las inscripciones de esa materia
        return (
            Enrollment.objects.filter(subject=self.subject)
            .select_related('student')
            .order_by('student__surname', 'student__name')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = self.subject
        return context

