from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connect import get_db
from app.database.models import Usuario

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("/")
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return [{"id": u.id, "nome": u.nome, "email": u.email, "telefone": u.telefone} for u in usuarios]

