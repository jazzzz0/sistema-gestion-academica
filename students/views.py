from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    """
    Función de vista para la página principal de la app students.
    Retorna una respuesta HTTP simple.
    """
    return HttpResponse("¡Hola desde la app Students!")