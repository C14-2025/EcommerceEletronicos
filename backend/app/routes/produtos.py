from fastapi import APIRouter, Depends, HTTPException
from fastapi import File, UploadFile, Form
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import List
import os
from datetime import datetime

from app.database.connect import get_db
from app.database.models import Produto, Usuario
from app.schemas.produto import ProdutoCreate, ProdutoOut, ProdutoUpdate
from app.config import IMAGENS_DIR 

router = APIRouter(prefix="/produtos", tags=["produtos"])

def verificar_admin(usuario_id: int, db: Session):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario or not usuario.is_admin:
        raise HTTPException(status_code=403, detail="Acesso negado. Usuário não é administrador.")
    return usuario

# Listar todos
@router.get("/", response_model=List[ProdutoOut])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(Produto).all()

# Buscar por ID
@router.get("/{produto_id}", response_model=ProdutoOut)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

# Criar produto
@router.post("/", response_model=ProdutoOut, status_code=201)
def criar_produto(
    usuario_id: int,
    nome: str = Form(...),
    descricao: str = Form(None),
    preco: float = Form(...),
    estoque: int = Form(...),
    imagem: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    verificar_admin(usuario_id, db)

    imagem_nome = None

    if imagem:
        # Usa o mesmo diretório estático da main.py
        pasta_imagens = IMAGENS_DIR

        # Garante que existe
        os.makedirs(pasta_imagens, exist_ok=True)

        # Nome único
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        nome_arquivo = f"{timestamp}_{imagem.filename}"

        # Caminho final
        caminho_completo = os.path.join(pasta_imagens, nome_arquivo)

        with open(caminho_completo, "wb") as f:
            f.write(imagem.file.read())

        imagem_nome = nome_arquivo

    novo = Produto(
        nome=nome,
        descricao=descricao,
        preco=preco,
        estoque=estoque,
        imagem=imagem_nome
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


# Atualizar produto
@router.put("/{produto_id}", response_model=ProdutoOut)
def atualizar_produto(produto_id: int, dados: ProdutoUpdate, usuario_id: int, db: Session = Depends(get_db)):
    verificar_admin(usuario_id, db)
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for campo, valor in dados.dict(exclude_unset=True).items():
        setattr(produto, campo, valor)
    db.commit()
    db.refresh(produto)
    return produto

# Deletar produto
@router.delete("/{produto_id}", status_code=204)
def deletar_produto(produto_id: int, usuario_id: int, db: Session = Depends(get_db)):
    verificar_admin(usuario_id, db)
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto)
    db.commit()
    return None
