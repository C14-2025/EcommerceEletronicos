import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from app.routes import usuarios
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate


# =====================================================
# Criar usuário com sucesso
# =====================================================
def test_criar_usuario_sucesso():
    mock_db = MagicMock()

    dados = UsuarioCreate(
        nome="Test User",
        email="teste@example.com",
        senha="123456",
        telefone="11999999999",
        is_admin=False,
        is_vendor=False
    )

    # Simular: nenhum usuário existente com mesmo email
    mock_db.query().filter().first.return_value = None

    novo_usuario = MagicMock(
        id=1,
        nome=dados.nome,
        email=dados.email,
        senha=dados.senha,
        telefone=dados.telefone,
        is_admin=False,
        is_vendor=False
    )

    # refresh devolve o objeto criado
    mock_db.refresh.side_effect = lambda obj: obj

    response = usuarios.criar_usuario(dados, db=mock_db)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    assert response.email == "teste@example.com"
    assert response.nome == "Test User"


# =====================================================
# Criar usuário com e-mail já cadastrado
# =====================================================
def test_criar_usuario_email_duplicado():
    mock_db = MagicMock()

    dados = UsuarioCreate(
        nome="Test User",
        email="duplicado@example.com",
        senha="123456",
        telefone="11999999999"
    )

    # Simular usuário existente
    mock_db.query().filter().first.return_value = MagicMock()

    with pytest.raises(HTTPException) as exc:
        usuarios.criar_usuario(dados, db=mock_db)

    assert exc.value.status_code == 400
    assert "Email já cadastrado" in exc.value.detail


# =====================================================
# Buscar usuário por ID com sucesso
# =====================================================
def test_buscar_usuario_sucesso():
    mock_db = MagicMock()

    mock_usuario = MagicMock(id=1, nome="User", email="user@example.com")
    mock_db.query().filter().first.return_value = mock_usuario

    response = usuarios.buscar_usuario(1, db=mock_db)

    assert response.id == 1
    assert response.nome == "User"


# =====================================================
# Buscar usuário inexistente
# =====================================================
def test_buscar_usuario_inexistente():
    mock_db = MagicMock()

    mock_db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as exc:
        usuarios.buscar_usuario(999, db=mock_db)

    assert exc.value.status_code == 404
    assert "Usuário não encontrado" in exc.value.detail


# =====================================================
# Atualizar usuário com sucesso
# =====================================================
def test_atualizar_usuario_sucesso():
    mock_db = MagicMock()

    mock_usuario = MagicMock()
    mock_db.query().filter().first.return_value = mock_usuario

    update_data = UsuarioUpdate(nome="Novo Nome")

    response = usuarios.atualizar_usuario(1, update_data, db=mock_db)

    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_usuario)

    assert mock_usuario.nome == "Novo Nome"
    assert response == mock_usuario


# =====================================================
# Atualizar usuário inexistente
# =====================================================
def test_atualizar_usuario_inexistente():
    mock_db = MagicMock()

    mock_db.query().filter().first.return_value = None

    update_data = UsuarioUpdate(nome="Novo Nome")

    with pytest.raises(HTTPException) as exc:
        usuarios.atualizar_usuario(999, update_data, db=mock_db)

    assert exc.value.status_code == 404


# =====================================================
# Deletar usuário com sucesso
# =====================================================
def test_deletar_usuario_sucesso():
    mock_db = MagicMock()

    mock_usuario = MagicMock()
    mock_db.query().filter().first.return_value = mock_usuario

    response = usuarios.deletar_usuario(1, db=mock_db)

    mock_db.delete.assert_called_once_with(mock_usuario)
    mock_db.commit.assert_called_once()
    assert response is None


# =====================================================
# Deletar usuário inexistente
# =====================================================
def test_deletar_usuario_inexistente():
    mock_db = MagicMock()

    mock_db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as exc:
        usuarios.deletar_usuario(999, db=mock_db)

    assert exc.value.status_code == 404
