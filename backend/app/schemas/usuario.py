from pydantic import BaseModel, ConfigDict
from typing import Optional

class UsuarioBase(BaseModel):
    nome: str
    email: str
    senha: str
    telefone: str
    is_admin: Optional[bool] = False
    is_vendor: Optional[bool] = False

class UsuarioCreate(UsuarioBase):
    is_admin: Optional[bool] = False
    is_vendor: Optional[bool] = False

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    telefone: Optional[str] = None
    is_admin: Optional[bool] = None
    is_vendor: Optional[bool] = None

class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str
    is_admin: bool
    is_vendor: bool
    model_config = ConfigDict(from_attributes=True)
