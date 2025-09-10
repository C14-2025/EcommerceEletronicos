from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connect import get_db
from app.database.models import Pedido

router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@router.get("/")
def listar_pedidos(db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).all()
    return [
        {
            "id": p.id,
            "usuario_id": p.usuario_id,
            "endereco_id": p.endereco_id,
            "data_pedido": p.data_pedido,
            "status": p.status,
        }
        for p in pedidos
    ]
