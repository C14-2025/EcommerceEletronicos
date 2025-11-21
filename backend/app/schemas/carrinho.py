from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class CarrinhoItemBase(BaseModel):
    produto_id: int
    quantidade: int

class CarrinhoItemCreate(CarrinhoItemBase):
    pass

class CarrinhoItemOut(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    produto_nome: str
    produto_preco: float

    model_config = ConfigDict(from_attributes=True)

class CarrinhoOut(BaseModel):
    id: int
    usuario_id: int
    itens: List[CarrinhoItemOut]

    model_config = ConfigDict(from_attributes=True)
