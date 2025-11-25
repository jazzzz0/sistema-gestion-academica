from django.views.generic import DetailView
from core.mixins import AdminRequiredMixin    
from students.models import Student

class StudentDetailView(AdminRequiredMixin, DetailView):
    model = Student
    template_name = "students/student_detail.html"

    def get_queryset(self):
        # Optimización para evitar N+1
        return Student.objects.select_related("user", "career")

