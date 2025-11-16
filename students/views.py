from typing import cast

from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from students.forms import StudentCreateForm


class StudentCreateView(FormView):
    form_class = StudentCreateForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:student_list')

    def form_valid(self, form: forms.BaseForm) -> HttpResponse:
        student_form = cast(StudentCreateForm, form)
        try:
            # El formulario se encarga de todo
            student_form.save()

            messages.success(self.request, 'Estudiante creado exitosamente.')
            return HttpResponseRedirect(self.get_success_url())

        except forms.ValidationError as e:
            # Si form.save() lanzó el error, lo capturamos
            student_form.add_error(None, e)
            return self.form_invalid(student_form)
