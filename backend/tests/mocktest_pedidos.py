import pytest
from unittest.mock import MagicMock
from app.routes import pedidos
from app.schemas.pedido import PedidoCreate, PedidoUpdate


# =====================================================
# Criar pedido com sucesso
# =====================================================
def test_criar_pedido_sucesso():
    mock_db = MagicMock()

    pedido_data = PedidoCreate(
        usuario_id=1,
        endereco_id=1,
        status="pendente"
    )

    mock_pedido = MagicMock()
    mock_pedido.usuario_id = pedido_data.usuario_id
    mock_pedido.endereco_id = pedido_data.endereco_id
    mock_pedido.status = pedido_data.status

    # Quando o refresh for chamado, devolve o objeto
    mock_db.refresh.side_effect = lambda obj: obj

    response = pedidos.criar_pedido(pedido_data, db=mock_db)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    assert response.usuario_id == 1
    assert response.endereco_id == 1
    assert response.status == "pendente"


# =====================================================
# Criar pedido com falha no commit
# =====================================================
def test_criar_pedido_falha_commit():
    mock_db = MagicMock()

    pedido_data = PedidoCreate(
        usuario_id=1,
        endereco_id=1,
        status="pendente"
    )

    mock_db.commit.side_effect = Exception("Erro no banco")

    with pytest.raises(Exception) as exc:
        pedidos.criar_pedido(pedido_data, db=mock_db)

    assert "Erro no banco" in str(exc.value)


# =====================================================
# Atualizar pedido com sucesso
# =====================================================
def test_atualizar_pedido_sucesso():
    mock_db = MagicMock()

    # Pedido existente simulado
    mock_pedido = MagicMock()
    mock_db.query().filter().first.return_value = mock_pedido

    dados_update = PedidoUpdate(status="enviado")

    response = pedidos.atualizar_pedido(1, dados_update, db=mock_db)

    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_pedido)

    assert mock_pedido.status == "enviado"
    assert response == mock_pedido


# =====================================================
# Atualizar pedido inexistente
# =====================================================
def test_atualizar_pedido_inexistente():
    mock_db = MagicMock()

    mock_db.query().filter().first.return_value = None

    dados_update = PedidoUpdate(status="enviado")

    with pytest.raises(Exception):
        pedidos.atualizar_pedido(999, dados_update, db=mock_db)


# =====================================================
# Deletar pedido com sucesso
# =====================================================
def test_deletar_pedido_sucesso():
    mock_db = MagicMock()

    mock_pedido = MagicMock()
    mock_db.query().filter().first.return_value = mock_pedido

    response = pedidos.deletar_pedido(1, db=mock_db)

    mock_db.delete.assert_called_once_with(mock_pedido)
    mock_db.commit.assert_called_once()
    assert response is None


# =====================================================
# Deletar pedido inexistente
# =====================================================
def test_deletar_pedido_inexistente():
    mock_db = MagicMock()

    mock_db.query().filter().first.return_value = None

    with pytest.raises(Exception):
        pedidos.deletar_pedido(999, db=mock_db)
