from django.views.generic import TemplateView

class AdminListView(TemplateView):
    template_name = "users/admins/admin_list.html"
    # Aquí iría la lógica para listar administradores           