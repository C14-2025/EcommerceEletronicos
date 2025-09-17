from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

# URL do banco (pegando de variável de ambiente ou default local)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:0000@localhost:5432/ecommerce"  # ajuste user/senha/db
)

# Cria o engine
engine = create_engine(DATABASE_URL, echo=True)

# Cria uma fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os models (se depois quiser usar ORM com classes Python)
Base = DeclarativeBase()

# Dependência para FastAPI (injeção em rotas)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()