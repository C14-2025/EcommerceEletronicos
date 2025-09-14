from tests import client
import pytest
from app.database.connect import get_db
from sqlalchemy import text


# Limpa a tabela antes de cada teste
@pytest.fixture(autouse=True)
def limpar_banco():
    db = next(get_db())
    db.execute(text("TRUNCATE pedidos RESTART IDENTITY CASCADE;"))
    db.commit()
    db.close()


# Criar pedido
def test_criar_pedido():
    response = client.post("/pedidos/", json={
        "usuario_id": 1,
        "endereco_id": 1,
        "status": "pendente"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["usuario_id"] == 1
    assert data["endereco_id"] == 1
    assert data["status"] == "pendente"


# Listar pedidos
def test_listar_pedidos():
    # cria antes
    client.post("/pedidos/", json={
        "usuario_id": 2,
        "endereco_id": 2,
        "status": "pendente"
    })

    response = client.get("/pedidos/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["usuario_id"] == 2


# Buscar pedido por ID existente
def test_buscar_pedido_por_id():
    client.post("/pedidos/", json={
        "usuario_id": 3,
        "endereco_id": 3,
        "status": "pendente"
    })

    response = client.get("/pedidos/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["usuario_id"] == 3

# Buscar pedido inexistente
def test_buscar_pedido_inexistente():
    response = client.get("/pedidos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado"


# Atualizar pedido existente
def test_atualizar_pedido():
    client.post("/pedidos/", json={
        "usuario_id": 4,
        "endereco_id": 4,
        "status": "pendente"
    })

    response = client.put("/pedidos/1", json={"status": "enviado"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "enviado"


# Deletar pedido existente
def test_deletar_pedido():
    client.post("/pedidos/", json={
        "usuario_id": 5,
        "endereco_id": 5,
        "status": "pendente"
    })

    response = client.delete("/pedidos/1")
    assert response.status_code == 204

    # confirma que foi excluído
    response = client.get("/pedidos/1")
    assert response.status_code==404