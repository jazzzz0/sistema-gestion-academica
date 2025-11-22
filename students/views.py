from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from students.forms import StudentCreateForm
from users.mixins import AdminRequiredMixin

from students.models import Student

class StudentCreateView(AdminRequiredMixin, FormView):
    form_class = StudentCreateForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:student-list')

    def form_valid(self, form: StudentCreateForm) -> HttpResponse:
        # El formulario se encarga de validar y guardar el estudiante
        student = form.save()

        if student:
            messages.success(self.request, f'Estudiante {student.full_name} creado correctamente.')
            return HttpResponseRedirect(self.get_success_url())
        else:
            # El guardado falló
            # El formulario ya tiene el error
            # Simplemente volvemos a mostrar el formulario
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Estudiante'
        context['action'] = 'Crear'
        return context


class StudentListView(AdminRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 20  # Requisito de paginación por defecto

    def get_queryset(self):
        # Optimizamos la consulta trayendo los datos del usuario relacionado
        # y ordenamos por apellido/nombre para una visualización consistente
        return Student.objects.select_related('user').all().order_by('surname', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Alumnos'
        return context