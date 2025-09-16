# store/utils/api.py
import requests

API_URL = "http://127.0.0.1:8000"  # Backend FastAPI

def get(endpoint: str):
    response = requests.get(f"{API_URL}{endpoint}")
    if response.status_code == 200:
        return response.json()
    return {"error": response.text}
