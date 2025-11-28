from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.database.connect import get_db
from sqlalchemy import text

client = TestClient(app)


@pytest.fixture(autouse=True)
def limpar_banco():
    db = next(get_db())
    db.execute(text("TRUNCATE produtos RESTART IDENTITY CASCADE;"))
    db.execute(text("TRUNCATE usuarios RESTART IDENTITY CASCADE;"))
    db.commit()
    db.close()


def criar_admin():
    client.post("/usuarios/", json={
        "nome": "Admin",
        "email": "admin@admin.com",
        "senha": "123",
        "telefone": "000",
        "is_admin": True
    })


def test_criar_produto():
    criar_admin()

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


def test_listar_produtos():
    criar_admin()

    client.post("/produtos/?usuario_id=1", data={
        "nome": "Mouse Gamer",
        "descricao": "Mouse com 6 botões",
        "preco": "150.0",
        "estoque": "20"
    })

    response = client.get("/produtos/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["nome"] == "Mouse Gamer"

