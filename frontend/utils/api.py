import requests

API_URL = "http://127.0.0.1:8000"  # URL do backend FastAPI

def get(endpoint: str):
    """Função genérica para requisições GET"""
    response = requests.get(f"{API_URL}{endpoint}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}
