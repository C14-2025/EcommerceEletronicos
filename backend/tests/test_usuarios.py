from tests import client


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