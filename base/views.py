from django.shortcuts import render
from django.views import View

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

class DashboardView(View):
    def get(self, request):
        return render(request, 'dashboard.html')
class ProfileView(View):
    def get(self, request):
        return render(request, 'profile.html')  