import pytest

def criar_admin(client):
    client.post("/usuarios/", json={
        "nome": "Admin",
        "email": "admin@admin.com",
        "senha": "123",
        "telefone": "000",
        "is_admin": True
    })


def test_criar_produto(client):
    criar_admin(client)

    response = client.post("/produtos/?usuario_id=1", data={
        "nome": "Teclado Mecânico",
        "descricao": "Teclado gamer RGB",
        "preco": "299.90",
        "estoque": "10"
    })

    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Teclado Mecânico"
    assert data["estoque"] == 10


def test_listar_produtos(client):
    criar_admin(client)

    client.post("/produtos/?usuario_id=1", data={
        "nome": "Mouse Gamer",
        "descricao": "Mouse com 6 botões",
        "preco": "150.0",
        "estoque": "20"
    })

    response = client.get("/produtos/")
    assert response.status_code == 200
    assert len(response.json()) == 1

