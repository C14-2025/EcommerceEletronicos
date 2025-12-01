# backend/tests/test_usuarios.py

def test_criar_usuario_duplicado(client):
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
        "email": "donatto@email.com",
        "senha": "abcdef",
        "telefone": "118888888"
    })
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Email já cadastrado"


def test_criar_usuario_sem_senha(client):
    response = client.post("/usuarios/", json={
        "nome": "SemSenha",
        "email": "semsenha@email.com",
        "telefone": "11988888888"
    })
    assert response.status_code == 422


def test_buscar_usuario_existente(client):
    client.post("/usuarios/", json={
        "nome": "Luiz",
        "email": "luiz@example.com",
        "senha": "123456",
        "telefone": "99999"
    })

    response = client.get("/usuarios/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["nome"] == "Luiz"
    assert data["email"] == "luiz@example.com"


def test_buscar_usuario_inexistente(client):
    response = client.get("/usuarios/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Usuário não encontrado"}


def test_criar_usuario_email_invalido(client):
    response = client.post("/usuarios/", json={
        "nome": "Teste",
        "email": "email_invalido",
        "senha": "123456",
        "telefone": "11999999999"
    })
    assert response.status_code == 201
