from pydantic import BaseModel, ConfigDict
from typing import Optional

class UsuarioBase(BaseModel):
    nome : str
    email : str
    senha : str
    telefone : str


class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(UsuarioBase):
    nome : Optional[str] = None
    email : Optional[str] = None
    senha : Optional[str] = None
    telefone : Optional[str] = None

class UsuarioOut(BaseModel):
    id: int
    nome : str
    email : str
    senha : str
    telefone : str
    model_config = ConfigDict(from_attributes=True)