import requests
from django.conf import settings

API_URL = "http://127.0.0.1:8000"

def get(endpoint: str):
    try:
        url = f"{API_URL}{endpoint}"
        print(f"🔵 Requisição GET para: {url}")
        resp = requests.get(url, timeout=10)
        print(f"🟢 Status: {resp.status_code}")

        if resp.status_code == 200:
            data = resp.json()
            print("🟣 Dados recebidos:")
            from pprint import pprint
            pprint(data)

            return data

        else:
            print(f"🔴 Erro da API: {resp.text}")
            return None

    except Exception as e:
        print(f"🚨 Erro na conexão com API: {e}")
        return None
