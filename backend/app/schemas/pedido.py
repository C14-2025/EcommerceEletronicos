from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# Base comum para Pedido
class PedidoBase(BaseModel):
    usuario_id: int
    endereco_id: int
    status: Optional[str] = "pendente"

# Schema para criação
class PedidoCreate(PedidoBase):
    pass

# Schema para atualização parcial
class PedidoUpdate(BaseModel):
    usuario_id: Optional[int] = None
    endereco_id: Optional[int] = None
    status: Optional[str] = None

# Schema para saída (resposta da API)
class PedidoOut(BaseModel):

    usuario_id: int
    endereco_id: int
    status: str
    data_pedido: datetime
    id: int

    model_config = ConfigDict(from_attributes=True)

