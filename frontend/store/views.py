from django.shortcuts import render
from .utils.api import get

def produtos(request):
    produtos = get("/produtos/")
    return render(request, "store/produtos.html", {"produtos": produtos})
