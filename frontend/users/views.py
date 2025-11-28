# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
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
            # 1️⃣ Tenta fazer login no backend
            response = requests.post(
                f"{BACKEND_URL}/auth/login",
                params={"email": email, "senha": senha}
            )

            if response.status_code == 200:
                data = response.json()
                usuario_login = data.get("usuario")

                # 2️⃣ Buscar informações completas do usuário
                try:
                    detalhes = requests.get(
                        f"{BACKEND_URL}/usuarios/{usuario_login['id']}"
                    )

                    if detalhes.status_code == 200:
                        usuario_completo = detalhes.json()
                    else:
                        usuario_completo = usuario_login  # fallback

                except Exception:
                    usuario_completo = usuario_login  # fallback

                # 3️⃣ Salva usuário completo na sessão
                request.session["usuario"] = usuario_completo

                messages.success(request, f"Bem-vindo(a), {usuario_completo['nome']}!")
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


def mudar_senha(request):
    usuario = request.session.get("usuario")
    if not usuario:
        messages.error(request, "Você precisa estar logado.")
        return redirect("login")

    if request.method == "POST":
        senha_atual = request.POST.get("senha_atual")
        nova_senha = request.POST.get("nova_senha")
        confirmar = request.POST.get("confirmar")

        if nova_senha != confirmar:
            messages.error(request, "As senhas não coincidem.")
            return redirect("mudar_senha")

        # 1️⃣ Validar senha atual usando o endpoint de login
        try:
            resp_login = requests.post(
                f"{BACKEND_URL}/auth/login",
                params={"email": usuario["email"], "senha": senha_atual}
            )

            if resp_login.status_code != 200:
                messages.error(request, "Senha atual incorreta.")
                return redirect("mudar_senha")

        except Exception as e:
            messages.error(request, f"Erro ao validar senha: {e}")
            return redirect("mudar_senha")

        # 2️⃣ Atualizar a senha no backend
        try:
            resp_update = requests.put(
                f"{BACKEND_URL}/usuarios/{usuario['id']}",
                json={"senha": nova_senha},
            )

            if resp_update.status_code == 200:
                # Atualiza sessão (não com a senha)
                request.session["usuario"] = usuario

                messages.success(request, "Senha alterada com sucesso!")
                return redirect("perfil")

            else:
                messages.error(request, f"Erro: {resp_update.text}")

        except Exception as e:
            messages.error(request, f"Erro ao conectar ao servidor: {e}")

    return render(request, "users/mudar_senha.html")



@require_POST
def deletar_conta(request):
    usuario = request.session.get("usuario")

    if not usuario:
        messages.error(request, "Você precisa estar logado.")
        return redirect("login")

    BACKEND_URL = "http://127.0.0.1:8000"

    try:
        resp = requests.delete(f"{BACKEND_URL}/usuarios/{usuario['id']}")

        if resp.status_code == 204:
            request.session.flush()
            messages.success(request, "Sua conta foi deletada com sucesso.")
            return redirect("home")

        else:
            messages.error(request, f"Erro ao deletar: {resp.text}")

    except Exception as e:
        messages.error(request, f"Erro ao conectar ao servidor: {e}")

    return redirect("perfil")


def admin_usuarios(request):
    usuario = request.session.get("usuario")

    if not usuario or not usuario.get("is_admin"):
        messages.error(request, "Acesso negado.")
        return redirect("home")

    from store.utils.api import get, API_URL
    usuarios = get("/usuarios/") or []

    return render(request, "users/usuarios_admin.html", {
        "usuarios": usuarios
    })


@require_POST
def admin_remover_usuario(request, usuario_id):
    usuario = request.session.get("usuario")

    if not usuario or not usuario.get("is_admin"):
        messages.error(request, "Acesso negado.")
        return redirect("home")

    import requests
    from store.utils.api import API_URL

    try:
        resp = requests.delete(f"{API_URL}/usuarios/{usuario_id}")
        if resp.status_code == 204:
            messages.success(request, "Usuário removido com sucesso.")
        else:
            messages.error(request, f"Erro ao remover: {resp.text}")
    except Exception as e:
        messages.error(request, f"Erro ao conectar ao backend: {e}")

    return redirect("admin_usuarios")
