from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


# ------------------------------
# Produto usado dentro de PedidoItemOut
# ------------------------------
class ProdutoSimples(BaseModel):
    id: int
    nome: str
    preco: float

    model_config = ConfigDict(from_attributes=True)


# ------------------------------
# PedidoItem
# ------------------------------
class PedidoItemOut(BaseModel):
    id: int
    produto: ProdutoSimples
    quantidade: int
    preco_unit: float

    model_config = ConfigDict(from_attributes=True)


# ------------------------------
# Pagamento
# ------------------------------
class PagamentoOut(BaseModel):
    valor: float
    metodo: str
    status: str
    data_pagamento: datetime

    model_config = ConfigDict(from_attributes=True)


# ------------------------------
# Pedido
# ------------------------------
class PedidoOut(BaseModel):
    id: int
    usuario_id: int
    endereco_id: int
    status: str
    data_pedido: datetime
    itens: List[PedidoItemOut]
    pagamento: Optional[PagamentoOut]

    model_config = ConfigDict(from_attributes=True)


# ------------------------------
# Criar/Atualizar
# ------------------------------
class PedidoBase(BaseModel):
    usuario_id: int
    endereco_id: int
    status: Optional[str] = "pendente"


class PedidoCreate(PedidoBase):
    pass


class PedidoUpdate(BaseModel):
    usuario_id: Optional[int] = None
    endereco_id: Optional[int] = None
    status: Optional[str] = None
