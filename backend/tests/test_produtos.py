from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.database.connect import get_db
from sqlalchemy import text

client = TestClient(app)


# Limpa a tabela antes de cada teste
@pytest.fixture(autouse=True)
def limpar_banco():
    db = next(get_db())
    db.execute(text("TRUNCATE produtos RESTART IDENTITY CASCADE;"))
    db.commit()
    db.close()


# Teste positivo - criar produto
def test_criar_produto():
    response = client.post("/produtos/", json={
        "nome": "Teclado Mecânico",
        "descricao": "Teclado gamer RGB",
        "preco": 299.90,
        "estoque": 10
    })
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["nome"] == "Teclado Mecânico"
    assert data["estoque"] == 10


# Teste positivo - listar produtos
def test_listar_produtos():
    # cria produto antes
    client.post("/produtos/", json={
        "nome": "Mouse Gamer",
        "descricao": "Mouse com 6 botões",
        "preco": 150.0,
        "estoque": 20
    })

    response = client.get("/produtos/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["nome"] == "Mouse Gamer"


# Buscar Produto Inexistente
def test_buscar_produto_inexistente():
    response = client.get("/produtos/999")  # id que não existe
    assert response.status_code == 404
    assert response.json()["detail"] == "Produto não encontrado"
