from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connect import get_db
from app.database.models import Usuario

router = APIRouter(prefix="/auth", tags=["autenticação"])

@router.post("/login")
def login(email: str, senha: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if usuario.senha != senha:
        raise HTTPException(status_code=401, detail="Senha incorreta")

    # (Você pode adicionar JWT ou session aqui futuramente)
    return {
        "message": "Login realizado com sucesso!",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
        },
    }
