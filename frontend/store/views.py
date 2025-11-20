from django.shortcuts import render, redirect
from django.contrib import messages
from .utils.api import get
from django.views.decorators.http import require_http_methods
from store.models import Produto
from .utils.api import API_URL  # base da API (ex: http://localhost:8000)
from django.views.decorators.http import require_POST
import requests
import pprint


def perfil(request):
    usuario = request.session.get("usuario")
    if not usuario:
        messages.error(request, "Você precisa estar logado para acessar o perfil.")
        return redirect("login")

    # Buscar pedidos do usuário no backend
    try:
        pedidos = get(f"/pedidos/?usuario_id={usuario['id']}")
    except Exception:
        pedidos = []

    return render(request, "store/perfil.html", {
        "usuario": usuario,
        "pedidos": pedidos
    })


def produtos(request):
    print(">>> ENTROU NA VIEW produtos()")
    produtos = get("/produtos/")
    pprint.pprint(produtos)  # Mostra no terminal
    return render(request, "store/produtos.html", {"produtos": produtos})

def home(request):
    print(">>> ENTROU NA HOME")
    produtos = get("/produtos/")
    pprint.pprint(produtos) 
    return render(request, "store/home.html", {"produtos": produtos})

def carrinho(request):
    usuario = request.session.get("usuario")
    if not usuario:
        return redirect("login")

    try:
        resp = get(f"/carrinho/?usuario_id={usuario['id']}")
        itens = resp["itens"]
    except Exception:
        itens = []

    total = sum(item["produto_preco"] * item["quantidade"] for item in itens)

    return render(request, "store/carrinho.html", {
        "itens": itens,
        "total": total
    })


def checkout(request):
    usuario = request.session.get("usuario")
    if not usuario:
        return redirect("login")

    # Buscar itens do carrinho REAL
    try:
        data = get(f"/carrinho/?usuario_id={usuario['id']}")
        itens = data["itens"]
    except Exception:
        itens = []

    total = sum(item["produto_preco"] * item["quantidade"] for item in itens)

    return render(request, "store/checkout.html", {
        "itens": itens,
        "total": total
    })

@require_POST
def finalizar_compra(request):
    usuario = request.session.get("usuario")
    if not usuario:
        return redirect("login")

    try:
        resp = requests.post(
            f"{API_URL}/carrinho/finalizar",
            params={"usuario_id": usuario["id"]}
        )

        if resp.status_code == 200:
            messages.success(request, "Compra finalizada com sucesso!")
            return redirect("perfil")

        else:
            messages.error(request, resp.json().get("detail", "Erro ao finalizar compra"))

    except Exception as e:
        messages.error(request, f"Erro ao conectar ao servidor: {e}")

    return redirect("checkout")


@require_POST
def adicionar_ao_carrinho(request, produto_id):
    usuario = request.session.get("usuario")

    if not usuario:
        messages.error(request, "Você precisa estar logado.")
        return redirect("login")

    try:
        resp = requests.post(
            f"{API_URL}/carrinho/adicionar",
            params={"usuario_id": usuario["id"]},
            json={"produto_id": produto_id, "quantidade": 1}
        )

        if resp.status_code == 200:
            messages.success(request, "Produto adicionado ao carrinho!")
        else:
            messages.error(request, resp.json().get("detail", "Erro ao adicionar item"))
    except Exception as e:
        messages.error(request, f"Erro ao conectar: {e}")

    return redirect("produtos")


def perfil(request):
    usuario = request.session.get("usuario")
    if not usuario:
        messages.error(request, "Você precisa estar logado para acessar o perfil.")
        return redirect("login")

    return render(request, "store/perfil.html", {"usuario": usuario})


def configuracoes(request):
    usuario = request.session.get("usuario")
    if not usuario:
        messages.error(request, "Você precisa estar logado para acessar as configurações.")
        return redirect("login")

    return render(request, "store/configuracoes.html", {"usuario": usuario})


@require_http_methods(["GET", "POST"])
def adicionar_produto_page(request):
    usuario = request.session.get("usuario")
    if not usuario or not usuario.get("is_admin"):
        messages.error(request, "Acesso negado: apenas administradores podem adicionar produtos.")
        return redirect("home")

    if request.method == "POST":
        nome = request.POST.get("nome")
        descricao = request.POST.get("descricao")
        preco = request.POST.get("preco")
        estoque = request.POST.get("estoque")
        imagem = request.FILES.get("imagem")

        try:
            # Se tiver imagem, monta um dicionário files; senão, envia só o JSON
            files = {"imagem": imagem} if imagem else None

            data = {
                "nome": nome,
                "descricao": descricao,
                "preco": preco,
                "estoque": estoque,
            }

            # 🔹 requests.post agora envia multipart (com arquivo)
            resp = requests.post(
                f"{API_URL}/produtos/?usuario_id={usuario['id']}",
                data=data,  # dados normais
                files=files,  # arquivo (se houver)
                timeout=10
            )

            if resp.status_code == 201:
                messages.success(request, f"Produto '{nome}' adicionado com sucesso!")
                return redirect("produtos")
            else:
                messages.error(request, f"Erro ao adicionar produto: {resp.text}")

        except Exception as e:
            messages.error(request, f"Erro de conexão com o servidor: {e}")

    return render(request, "store/adicionar_produto.html", {"usuario": usuario})


@require_http_methods(["GET", "POST"])
def remover_produto_page(request):
    usuario = request.session.get("usuario")

    if not usuario or not usuario.get("is_admin"):
        messages.error(request, "Acesso negado: somente administradores podem remover produtos.")
        return redirect("home")

    # GET → Apenas listar os produtos
    produtos = get("/produtos/")

    return render(request, "store/remover_produto.html", {
        "produtos": produtos,
        "usuario": usuario
    })


@require_POST
def remover_produto(request, produto_id):
    usuario = request.session.get("usuario")

    if not usuario or not usuario.get("is_admin"):
        messages.error(request, "Acesso negado.")
        return redirect("home")

    try:
        resp = requests.delete(
            f"{API_URL}/produtos/{produto_id}?usuario_id={usuario['id']}",
            timeout=10
        )

        if resp.status_code == 204:
            messages.success(request, "Produto removido com sucesso!")
        else:
            messages.error(request, f"Erro ao remover produto: {resp.text}")

    except Exception as e:
        messages.error(request, f"Erro ao conectar ao servidor: {e}")

    return redirect("remover_produto")


