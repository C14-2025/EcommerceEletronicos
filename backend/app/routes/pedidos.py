from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database.connect import get_db
from app.database.models import Pedido
from app.schemas.pedido import PedidoCreate, PedidoUpdate, PedidoOut

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


# ==========================
# Listar todos os pedidos
# ==========================
@router.get("/", response_model=List[PedidoOut])
def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(Pedido).all()


# ==========================
# Buscar pedido por ID
# ==========================
@router.get("/{pedido_id}", response_model=PedidoOut)
def buscar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido


# ==========================
# Criar um novo pedido
# ==========================
@router.post("/", response_model=PedidoOut, status_code=201)
def criar_pedido(dados: PedidoCreate, db: Session = Depends(get_db)):
    novo = Pedido(**dados.dict())
    novo.data_pedido = datetime.utcnow()
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


# ==========================
# Atualizar um pedido existente
# ==========================
@router.put("/{pedido_id}", response_model=PedidoOut)
def atualizar_pedido(pedido_id: int, dados: PedidoUpdate, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    for campo, valor in dados.dict(exclude_unset=True).items():
        setattr(pedido, campo, valor)

    db.commit()
    db.refresh(pedido)
    return pedido


# ==========================
# Deletar um pedido
# ==========================
@router.delete("/{pedido_id}", status_code=204)
def deletar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    db.delete(pedido)
    db.commit()
<<<<<<< HEAD
    return None
=======
    return None
>>>>>>> origin/main
