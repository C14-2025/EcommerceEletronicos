from fastapi import FastAPI
from app.routes import usuarios, produtos, pedidos, pagamentos
from app.database.connect import engine, Base

# Cria tabelas no banco caso não existam
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Inclui rotas
app.include_router(usuarios.router)
app.include_router(produtos.router)
app.include_router(pedidos.router)
app.include_router(pagamentos.router)

@app.get("/")
def root():
    return {"message": "API do Ecommerce online!"}
