import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.connect import Base, get_db
from app.database.models import Pagamento


# -----------------------------
# CONFIGURAÇÃO DO BANCO DE TESTE
# -----------------------------

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # necessário para SQLite
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_test():
    """Cria banco limpo para cada teste."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()


# -----------------------------
# OVERRIDE DO get_db DO FASTAPI
# -----------------------------

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# -----------------------------
# TESTE DO ENDPOINT /pagamentos/
# -----------------------------

def test_listar_pagamentos(db_test):
    # Inserir dados fake no banco
    pagamento = Pagamento(
        pedido_id=1,
        valor=99.90,
        metodo="cartao",
        status="pago",
        data_pagamento=None
    )

    db_test.add(pagamento)
    db_test.commit()

    # Chamada ao endpoint
    response = client.get("/pagamentos/")
    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["pedido_id"] == 1
    assert data[0]["valor"] == 99.9  
    assert data[0]["metodo"] == "cartao"
    assert data[0]["status"] == "pago"
