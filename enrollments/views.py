from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Primera vista de enrollments")