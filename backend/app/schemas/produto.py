from pydantic import BaseModel, ConfigDict
from typing import Optional

# Base comum para Produto
class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    estoque: int
    imagem: Optional[str] = None  # 🔹 novo campo opcional

# Schema para criação
class ProdutoCreate(ProdutoBase):
    pass

# Schema para atualização parcial
class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    estoque: Optional[int] = None

# Schema para saída (resposta da API)
class ProdutoOut(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None
    preco: float
    estoque: int
    imagem: Optional[str] = None
    compras: int = 0 

    model_config = ConfigDict(from_attributes=True)
