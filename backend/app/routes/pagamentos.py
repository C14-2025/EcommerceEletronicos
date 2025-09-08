from fastapi import APIRouter

router = APIRouter(prefix="/pagamentos", tags=["pagamentos"])

@router.get("/")
def listar_pagamentos():
    return [{"id": 1, "pedido_id": 1, "status": "aguardando"}]
