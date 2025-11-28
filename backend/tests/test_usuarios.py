from tests import client
from unittest.mock import patch


# Teste para Verificar se o usuário possui email DUPLICADO
def test_criar_usuario_duplicado():
    # Cria um usuário inicial
    response1 = client.post("/usuarios/", json={
        "nome": "Donatto",
        "email": "donatto@email.com",
        "senha": "123456",
        "telefone": "119999999"
    })
    assert response1.status_code == 201

    # Tenta criar outro usuário com o mesmo email
    response2 = client.post("/usuarios/", json={
        "nome": "Outro",
        "email": "donatto@email.com",  # duplicado
        "senha": "abcdef",
        "telefone": "118888888"
    })
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Email já cadastrado"


# Teste para Criar usuário sem campo obrigatório
def test_criar_usuario_sem_senha():
    # Tenta criar usuário sem senha
    response = client.post("/usuarios/", json={
        "nome": "SemSenha",
        "email": "semsenha@email.com",
        "telefone": "11988888888"
    })

    # Deve retornar erro de validação
    assert response.status_code == 422



# Teste para buscar usuário inexistente - REFATORADO
def test_buscar_usuario_existente(client):
    mock_user = {"id": 1, "nome": "Luiz", "email": "luiz@example.com"}

    # mockando o service chamado pela rota
    with patch("app.routes.usuarios.usuario_service.buscar_por_id", return_value=mock_user):
        response = client.get("/usuarios/1")

    assert response.status_code == 200
    assert response.json() == mock_user


def test_buscar_usuario_inexistente(client):
    with patch("app.routes.usuarios.usuario_service.buscar_por_id", return_value=None):
        response = client.get("/usuarios/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Usuário não encontrado"}



# Criar usuário com email inválido
def test_criar_usuario_email_invalido():
    response = client.post("/usuarios/", json={
        "nome": "Teste",
        "email": "email_invalido",
        "senha": "123456",
        "telefone": "11999999999"
    })
    assert response.status_code == 201

