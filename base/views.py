from django.shortcuts import render

from django.shortcuts import render

def inicio(request):
    return render(request, "index.html")
