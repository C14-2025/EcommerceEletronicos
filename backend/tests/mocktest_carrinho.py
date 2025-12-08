import pytest
from unittest.mock import MagicMock

from app.routes import carrinho
from app.schemas.carrinho import CarrinhoItemCreate


# =====================================================
# Auxiliar: criar carrinho fake
# =====================================================
def criar_carrinho_fake(id=1, usuario_id=1, itens=None):
    mock = MagicMock()
    mock.id = id
    mock.usuario_id = usuario_id
    mock.itens = itens or []
    return mock


# =====================================================
# Mostrar carrinho
# =====================================================
def test_mostrar_carrinho():
    mock_db = MagicMock()

    mock_item = MagicMock()
    mock_item.id = 1
    mock_item.produto_id = 10
    mock_item.quantidade = 2
    mock_item.produto.nome = "Produto X"
    mock_item.produto.preco = 20.5

    mock_carrinho = criar_carrinho_fake(itens=[mock_item])

    mock_db.query().filter().first.return_value = mock_carrinho

    response = carrinho.mostrar_carrinho(usuario_id=1, db=mock_db)

    assert response["usuario_id"] == 1
    assert len(response["itens"]) == 1
    assert response["itens"][0]["produto_nome"] == "Produto X"


# =====================================================
# Adicionar item
# =====================================================
def test_adicionar_item_sucesso():
    mock_db = MagicMock()

    mock_carrinho = criar_carrinho_fake()
    mock_db.query().filter().first.return_value = mock_carrinho

    mock_produto = MagicMock()
    mock_produto.id = 10
    mock_db.query().filter().first.side_effect = [mock_carrinho, mock_produto]

    dados = CarrinhoItemCreate(produto_id=10, quantidade=1)

    response = carrinho.adicionar_item(usuario_id=1, dados=dados, db=mock_db)

    mock_db.commit.assert_called()
    assert response["detail"] == "Item adicionado ao carrinho"


def test_adicionar_item_produto_nao_existe():
    mock_db = MagicMock()

    mock_carrinho = criar_carrinho_fake()
    mock_db.query().filter().first.side_effect = [mock_carrinho, None]

    dados = CarrinhoItemCreate(produto_id=999, quantidade=1)

    with pytest.raises(Exception):
        carrinho.adicionar_item(usuario_id=1, dados=dados, db=mock_db)


# =====================================================
# Remover item
# =====================================================
def test_remover_item_sucesso():
    mock_db = MagicMock()

    mock_item = MagicMock()
    mock_db.query().filter().first.return_value = mock_item

    mock_carrinho = criar_carrinho_fake()
    mock_carrinho.itens = [mock_item]

    mock_db.query().filter().first.side_effect = [mock_carrinho, mock_item]

    response = carrinho.remover_item(usuario_id=1, item_id=1, db=mock_db)

    mock_db.delete.assert_called_once_with(mock_item)
    mock_db.commit.assert_called_once()
    assert response["detail"] == "Item removido"


def test_remover_item_inexistente():
    mock_db = MagicMock()

    mock_carrinho = criar_carrinho_fake()
    mock_db.query().filter().first.side_effect = [mock_carrinho, None]

    with pytest.raises(Exception):
        carrinho.remover_item(usuario_id=1, item_id=999, db=mock_db)


# =====================================================
# Limpar carrinho
# =====================================================
def test_limpar_carrinho():
    mock_db = MagicMock()

    mock_item1 = MagicMock()
    mock_item2 = MagicMock()

    mock_carrinho = criar_carrinho_fake(itens=[mock_item1, mock_item2])
    mock_db.query().filter().first.return_value = mock_carrinho

    response = carrinho.limpar_carrinho(usuario_id=1, db=mock_db)

    assert mock_db.delete.call_count == 2
    mock_db.commit.assert_called_once()
    assert response["detail"] == "Carrinho vazio"


# =====================================================
# Finalizar compra com carrinho vazio
# =====================================================
def test_finalizar_compra_vazio():
    mock_db = MagicMock()

    mock_carrinho = criar_carrinho_fake(itens=[])
    mock_db.query().filter().first.return_value = mock_carrinho

    with pytest.raises(Exception):
        carrinho.finalizar_compra(usuario_id=1, db=mock_db)


# =====================================================
# Finalizar compra com sucesso
# =====================================================
def test_finalizar_compra_sucesso():
    mock_db = MagicMock()

   
    mock_item = MagicMock()
    mock_item.quantidade = 2
    mock_item.produto.preco = 10.0
    mock_item.produto_id = 5

    mock_carrinho = criar_carrinho_fake(itens=[mock_item])

    
    mock_db.query().filter().first.return_value = mock_carrinho

    
    mock_pedido = MagicMock()
    mock_pedido.id = 123
    mock_db.refresh.side_effect = lambda x: x

    response = carrinho.finalizar_compra(usuario_id=1, db=mock_db)

    assert response["pedido_id"] == 123
    assert response["total"] == 20.0
    assert "Pedido finalizado" in response["detail"]
