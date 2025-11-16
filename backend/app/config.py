import os

# Caminho absoluto padronizado para imagens
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGENS_DIR = os.path.join(BASE_DIR, "static", "imagens")

# Garante que a pasta exista
os.makedirs(IMAGENS_DIR, exist_ok=True)
