# Criado para definição de configs e fixtures 
import pytest
from sqlalchemy import text
from app.database.connect import get_db

# Função que prepara a base de testes
@pytest.fixture(autouse=True)
def limpar_banco():
    db = next(get_db())
    # Limpa as tabelas principais e reseta os IDs
    db.execute(text("TRUNCATE usuarios RESTART IDENTITY CASCADE;"))
    db.execute(text("TRUNCATE produtos RESTART IDENTITY CASCADE;"))
    db.execute(text("TRUNCATE pedidos RESTART IDENTITY CASCADE;"))
    db.commit()
    yield
    db.close()