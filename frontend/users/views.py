# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests

BACKEND_URL = "http://127.0.0.1:8000"  # Porta do FastAPI

def signup_view(request):
    from .forms import SignupForm

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                response = requests.post(f"{BACKEND_URL}/usuarios/", json=data)
                if response.status_code == 201:
                    messages.success(request, "Usuário cadastrado com sucesso!")
                    return redirect("login")
                else:
                    messages.error(request, f"Erro ao cadastrar: {response.text}")
            except Exception as e:
                messages.error(request, f"Falha de conexão com o servidor: {e}")
    else:
        form = SignupForm()

    return render(request, "users/signup.html", {"form": form})

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        if not email or not senha:
            messages.error(request, "Por favor, preencha todos os campos.")
            return redirect("login")

        try:
            response = requests.post(
                f"{BACKEND_URL}/auth/login",
                params={"email": email, "senha": senha}
            )

            if response.status_code == 200:
                data = response.json()
                usuario = data.get("usuario")

                # Armazena o usuário na sessão
                request.session["usuario"] = usuario
                messages.success(request, f"Bem-vindo(a), {usuario['nome']}!")

                return redirect("home")

            elif response.status_code in (401, 404):
                erro = response.json().get("detail", "Credenciais inválidas.")
                messages.error(request, erro)
            else:
                messages.error(request, f"Erro inesperado: {response.status_code}")

        except Exception as e:
            messages.error(request, f"Erro ao conectar com o backend: {e}")

    return render(request, "users/login.html")


def logout_view(request):
    request.session.flush()  # limpa sessão
    messages.info(request, "Você saiu da sua conta.")
    return redirect("home")
