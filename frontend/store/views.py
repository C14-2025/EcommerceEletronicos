from django.shortcuts import render, redirect
from django.contrib import messages
from .utils.api import get
from django.views.decorators.http import require_POST
import requests

def produtos(request):
    produtos = get("/produtos/")
    return render(request, "store/produtos.html", {"produtos": produtos})

def home(request):
    return render(request, 'store/home.html')

def carrinho(request):
    # Simulação: carrinho guardado na sessão
    carrinho = request.session.get("carrinho", [])
    usuario = request.session.get("usuario")

    if not usuario:
        messages.info(request, "Você precisa estar logado para ver seu carrinho.")
        return redirect("login")

    total = sum(item["preco"] * item["quantidade"] for item in carrinho)

    return render(request, "store/carrinho.html", {
        "carrinho": carrinho,
        "total": total,
        "usuario": usuario
    })

def checkout(request):
    return render(request, "store/checkout.html")

@require_POST
def adicionar_ao_carrinho(request, produto_id):
    produtos = get(f"/produtos/{produto_id}")
    if not produtos:
        messages.error(request, "Produto não encontrado.")
        return redirect("produtos")

    carrinho = request.session.get("carrinho", [])
    # Verifica se o produto já está no carrinho
    for item in carrinho:
        if item["id"] == produtos["id"]:
            item["quantidade"] += 1
            break
    else:
        carrinho.append({
            "id": produtos["id"],
            "nome": produtos["nome"],
            "preco": float(produtos["preco"]),
            "quantidade": 1
        })

    request.session["carrinho"] = carrinho
    messages.success(request, f"{produtos['nome']} foi adicionado ao carrinho!")
    return redirect("produtos")
