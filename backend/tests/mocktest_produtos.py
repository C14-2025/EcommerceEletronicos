import pytest
from unittest.mock import MagicMock, patch
from app.routes import produtos
from app.schemas.produto import ProdutoCreate

def test_criar_produto_sucesso():
    # Mock da sessão do banco
    mock_db = MagicMock()

    # Dados de entrada (simula o JSON da requisição)
    produto_data = ProdutoCreate(
        nome="Mouse Gamer",
        descricao="RGB, 16000 DPI",
        preco=199.90,
        estoque=50
    )

    # Mock do objeto produto salvo no banco
    mock_produto = MagicMock()
    mock_produto.nome = produto_data.nome
    mock_produto.preco = produto_data.preco
    mock_produto.estoque = produto_data.estoque

    # Configura o comportamento do refresh (quando o banco atualiza o objeto)
    mock_db.refresh.side_effect = lambda obj: obj

    # Executa a função que queremos testar
    response = produtos.criar_produto(produto_data, db=mock_db)

    # 🔎 Asserções de comportamento
    mock_db.add.assert_called_once()      # Produto foi adicionado ao banco
    mock_db.commit.assert_called_once()   # Commit foi chamado
    mock_db.refresh.assert_called_once()  # Refresh foi chamado

    # 🔎 Asserções de valores retornados
    assert response.nome == "Mouse Gamer"
    assert response.preco == 199.90
    assert response.estoque == 50


def test_criar_produto_falha_commit():
    # Mock da sessão do banco
    mock_db = MagicMock()

    produto_data = ProdutoCreate(
        nome="Teclado Mecânico",
        descricao="Switch Red",
        preco=399.90,
        estoque=20
    )

    # Simula falha no commit
    mock_db.commit.side_effect = Exception("Erro no banco")

    # Executa a função e espera exceção
    with pytest.raises(Exception) as exc:
        produtos.criar_produto(produto_data, db=mock_db)

    # 🔎 Asserção: erro realmente ocorreu
    assert "Erro no banco" in str(exc.value)
