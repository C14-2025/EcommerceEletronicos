import pytest

def criar_usuario_padrao(client):
    client.post("/usuarios/", json={
        "nome": "User",
        "email": "user@user.com",
        "senha": "123",
        "telefone": "000"
    })


def test_criar_pedido(client):
    criar_usuario_padrao(client)

    response = client.post("/pedidos/", json={
        "usuario_id": 1,
        "endereco_id": 1,
        "status": "pendente"
    })

    assert response.status_code == 201
    assert response.json()["usuario_id"] == 1


def test_listar_pedidos(client):
    criar_usuario_padrao(client)

    client.post("/pedidos/", json={
        "usuario_id": 1,
        "endereco_id": 1,
        "status": "pendente"
    })

    response = client.get("/pedidos/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_buscar_pedido_por_id(client):
    criar_usuario_padrao(client)

    client.post("/pedidos/", json={
        "usuario_id": 1,
        "endereco_id": 1,
        "status": "pendente"
    })

    response = client.get("/pedidos/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_buscar_pedido_inexistente(client):
    response = client.get("/pedidos/999")
    assert response.status_code == 404


def test_atualizar_pedido(client):
    criar_usuario_padrao(client)

    client.post("/pedidos/", json={
        "usuario_id": 1,
        "endereco_id": 1,
        "status": "pendente"
    })

    resp = client.put("/pedidos/1", json={"status": "enviado"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "enviado"


def test_deletar_pedido(client):
    criar_usuario_padrao(client)

    client.post("/pedidos/", json={
        "usuario_id": 1,
        "endereco_id": 1,
        "status": "pendente"
    })

    resp = client.delete("/pedidos/1")
    assert resp.status_code == 204
