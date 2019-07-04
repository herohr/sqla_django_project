from django.shortcuts import render, redirect
from django.views import View

# Create your views here.
from django.shortcuts import render


class RegisterView(View):
    def get(self, request):
        return render(request, "user-register.html")


class LoginView(View):
    def get(self, request):
        return render(request, "user-login.html")
