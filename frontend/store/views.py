from django.shortcuts import render
from .utils.api import get

def produtos(request):
    produtos = get("/produtos/")
    return render(request, "store/produtos.html", {"produtos": produtos})

def home(request):
    return render(request, 'store/home.html')

def carrinho(request):
    # Aqui futuramente você vai integrar com sessão ou backend para mostrar itens
    return render(request, "store/carrinho.html")

def checkout(request):
    return render(request, "store/checkout.html")