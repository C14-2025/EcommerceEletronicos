import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base
from app.main import app

from fastapi.testclient import TestClient

# Banco de testes SQLite
TEST_DATABASE_URL = "sqlite:///./test.db"

engine_test = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(autouse=True)
def setup_database():
    # recria as tabelas para cada teste
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)
    yield


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine_test)
    return TestClient(app)
