from fastapi.testclient import TestClient
from app.main import app

# Cliente de teste disponível para todos os módulos
client = TestClient(app) 