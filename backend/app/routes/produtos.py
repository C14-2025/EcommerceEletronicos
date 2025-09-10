from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connect import get_db
from app.database.models import Produto

router = APIRouter(prefix="/produtos", tags=["produtos"])

@router.get("/")
def listar_produtos(db: Session = Depends(get_db)):
    produtos = db.query(Produto).all()
    return [
        {"id": p.id, "nome": p.nome, "descricao": p.descricao, "preco": float(p.preco), "estoque": p.estoque}
        for p in produtos
    ]
