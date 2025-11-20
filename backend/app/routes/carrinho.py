from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime


from app.database.connect import get_db
from app.database.models import Carrinho, CarrinhoItem, Produto
from app.database.models import Pedido, PedidoItem, Pagamento
from app.schemas.carrinho import CarrinhoItemCreate, CarrinhoOut

router = APIRouter(prefix="/carrinho", tags=["carrinho"])

# Util: obter carrinho do usuário
def obter_carrinho(db: Session, usuario_id: int):
    carrinho = db.query(Carrinho).filter(Carrinho.usuario_id == usuario_id).first()
    if not carrinho:
        carrinho = Carrinho(usuario_id=usuario_id)
        db.add(carrinho)
        db.commit()
        db.refresh(carrinho)
    return carrinho

# ================
# Ver carrinho
# ================
@router.get("/", response_model=CarrinhoOut)
def mostrar_carrinho(usuario_id: int, db: Session = Depends(get_db)):
    carrinho = obter_carrinho(db, usuario_id)

    itens_out = []
    for item in carrinho.itens:
        itens_out.append({
            "id": item.id,
            "produto_id": item.produto_id,
            "quantidade": item.quantidade,
            "produto_nome": item.produto.nome,
            "produto_preco": float(item.produto.preco)
        })

    return {
        "id": carrinho.id,
        "usuario_id": carrinho.usuario_id,
        "itens": itens_out
    }

# ================
# Adicionar item
# ================
@router.post("/adicionar")
def adicionar_item(usuario_id: int, dados: CarrinhoItemCreate, db: Session = Depends(get_db)):
    carrinho = obter_carrinho(db, usuario_id)

    produto = db.query(Produto).filter(Produto.id == dados.produto_id).first()
    if not produto:
        raise HTTPException(404, "Produto não encontrado")

    item = (
        db.query(CarrinhoItem)
        .filter(CarrinhoItem.carrinho_id == carrinho.id)
        .filter(CarrinhoItem.produto_id == dados.produto_id)
        .first()
    )

    if item:
        item.quantidade += dados.quantidade
    else:
        item = CarrinhoItem(
            carrinho_id=carrinho.id,
            produto_id=dados.produto_id,
            quantidade=dados.quantidade
        )
        db.add(item)

    db.commit()
    return {"detail": "Item adicionado ao carrinho"}

# ================
# Remover item
# ================
@router.delete("/remover/{item_id}")
def remover_item(usuario_id: int, item_id: int, db: Session = Depends(get_db)):
    carrinho = obter_carrinho(db, usuario_id)

    item = db.query(CarrinhoItem).filter(
        CarrinhoItem.id == item_id,
        CarrinhoItem.carrinho_id == carrinho.id
    ).first()

    if not item:
        raise HTTPException(404, "Item não encontrado")

    db.delete(item)
    db.commit()

    return {"detail": "Item removido"}

# ================
# Limpar carrinho
# ================
@router.delete("/limpar")
def limpar_carrinho(usuario_id: int, db: Session = Depends(get_db)):
    carrinho = obter_carrinho(db, usuario_id)

    for item in carrinho.itens:
        db.delete(item)

    db.commit()
    return {"detail": "Carrinho vazio"}


@router.post("/finalizar")
def finalizar_compra(usuario_id: int, metodo: str = "simulado", db: Session = Depends(get_db)):
    # Garantir carrinho existente
    carrinho = obter_carrinho(db, usuario_id)

    if not carrinho.itens:
        raise HTTPException(400, "Carrinho está vazio")

    # Criar pedido
    novo_pedido = Pedido(
        usuario_id=usuario_id,
        endereco_id=1,  # Simulação — você pode adicionar Endereco depois
        data_pedido=datetime.utcnow(),
        status="pendente"
    )

    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    total = 0

    # Criar itens do pedido com base no carrinho
    for item in carrinho.itens:
        pedido_item = PedidoItem(
            pedido_id=novo_pedido.id,
            produto_id=item.produto_id,
            quantidade=item.quantidade,
            preco_unit=item.produto.preco
        )
        total += float(item.produto.preco) * item.quantidade
        db.add(pedido_item)

    db.commit()

    # Criar pagamento simulado
    pagamento = Pagamento(
        pedido_id=novo_pedido.id,
        valor=total,
        metodo=metodo,
        status="pago",  # simulação!
        data_pagamento=datetime.utcnow()
    )

    db.add(pagamento)
    db.commit()

    # Limpar carrinho
    for item in carrinho.itens:
        db.delete(item)

    db.commit()

    return {
        "detail": "Pedido finalizado com sucesso!",
        "pedido_id": novo_pedido.id,
        "total": total
    }