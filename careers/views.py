from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView


# TODO: Necesitamos un AdminRequiredMixin para que esta vista solo pueda ser utilizada por los admins
class CareerCreateView(LoginRequiredMixin, CreateView):
    pass
