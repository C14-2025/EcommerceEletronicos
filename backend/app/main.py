from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import usuarios, produtos, pedidos, pagamentos, auth
from app.database.connect import engine, Base
from app.config import IMAGENS_DIR
import os

# Cria tabelas no banco caso não existam
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Rota pública para acessar as imagens
app.mount("/static/imagens", StaticFiles(directory=IMAGENS_DIR), name="imagens")

# Inclui rotas
app.include_router(usuarios.router)
app.include_router(produtos.router)
app.include_router(pedidos.router)
app.include_router(pagamentos.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "API do Ecommerce online!"}
