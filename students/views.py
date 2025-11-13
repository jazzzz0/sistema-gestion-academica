from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentCreateForm

def create_student(request):
    """
    Vista para crear un nuevo alumno junto con su usuario asociado.
    """
    if request.method == "POST":
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Alumno creado correctamente.")
            return redirect("students:success")  # redirige a la vista de éxito
        else:
            messages.error(request, "Por favor, corrija los errores del formulario.")
    else:
        form = StudentCreateForm()

    return render(request, "students/create_student.html", {"form": form})


def success_view(request):
    """
    Vista de confirmación tras la creación exitosa del alumno.
    """
    return render(request, "students/success.html")
    return render(request, "students/create_student.html", {"form": form})