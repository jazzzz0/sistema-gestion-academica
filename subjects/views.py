from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from users.mixins import AdminRequiredMixin
from subjects.forms import SubjectForm
from subjects.models import Subject



class SubjectCreateView(AdminRequiredMixin, CreateView):
  
    model = Subject
    form_class = SubjectForm
    template_name = "subjects/subject_form.html"
    success_url = reverse_lazy("subjects:subject_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Materia'
        context['action'] = 'Crear'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Materia {form.cleaned_data["name"]} creada correctamente.'
        )
        return response

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
    
