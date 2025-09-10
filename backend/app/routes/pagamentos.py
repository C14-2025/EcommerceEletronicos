from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connect import get_db
from app.database.models import Pagamento

router = APIRouter(prefix="/pagamentos", tags=["pagamentos"])

@router.get("/")
def listar_pagamentos(db: Session = Depends(get_db)):
    pagamentos = db.query(Pagamento).all()
    return [
        {
            "id": pg.id,
            "pedido_id": pg.pedido_id,
            "valor": float(pg.valor),
            "metodo": pg.metodo,
            "status": pg.status,
            "data_pagamento": pg.data_pagamento,
        }
        for pg in pagamentos
    ]
