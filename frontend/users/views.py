# users/views.py
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from .forms import SignupForm
import requests

BACKEND_URL = "http://127.0.0.1:8000"  # Porta do FastAPI (ajuste se for diferente)

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                response = requests.post(f"{BACKEND_URL}/usuarios/", json=data)
                if response.status_code == 201:
                    messages.success(request, "Usuário cadastrado com sucesso!")
                    form = SignupForm()  # limpa o form
                else:
                    messages.error(request, f"Erro ao cadastrar: {response.text}")
            except Exception as e:
                messages.error(request, f"Falha de conexão com o servidor: {e}")
    else:
        form = SignupForm()

    return render(request, "users/signup.html", {"form": form})

def login_view(request):
    return render(request, "users/login.html")

def logout_view(request):
    return HttpResponse("Logout (placeholder)")