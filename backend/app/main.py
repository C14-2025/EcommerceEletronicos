from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import usuarios, produtos, pedidos, pagamentos, auth
from app.database.connect import engine, Base
import os

# Cria tabelas no banco caso não existam
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Diretório onde as imagens ficarão salvas
IMAGENS_DIR = os.path.join(os.path.dirname(__file__), "static", "imagens")

# Garante que a pasta exista
os.makedirs(IMAGENS_DIR, exist_ok=True)

# Rota pública para acessar as imagens
app.mount("/imagens", StaticFiles(directory=IMAGENS_DIR), name="imagens")

# Inclui rotas
app.include_router(usuarios.router)
app.include_router(produtos.router)
app.include_router(pedidos.router)
app.include_router(pagamentos.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "API do Ecommerce online!"}
