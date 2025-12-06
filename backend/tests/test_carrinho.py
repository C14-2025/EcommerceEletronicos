import pytest


def criar_produto_padrao(client):
    client.post("/produtos/", json={
        "nome": "Produto Teste",
        "descricao": "teste",
        "preco": 10.0,
        "estoque": 100
    })


# ================================
# 1 — Ver carrinho vazio
# ================================
def test_ver_carrinho_vazio(client):
    response = client.get("/carrinho/?usuario_id=1")
    assert response.status_code == 200
    assert response.json()["itens"] == []




# ==========================================
# 3 — Carrinho deve retornar item adicionado
# ==========================================
def test_listar_itens_do_carrinho(client):
    criar_produto_padrao(client)

    client.post("/carrinho/adicionar?usuario_id=1", json={
        "produto_id": 1,
        "quantidade": 1
    })

    response = client.get("/carrinho/?usuario_id=1")
    assert response.status_code == 200

    itens = response.json()["itens"]

    assert len(itens) == 1
    assert itens[0]["produto_id"] == 1
    assert itens[0]["quantidade"] == 1


# ===================================
# 5 — Limpar carrinho
# ===================================
def test_limpar_carrinho(client):
    criar_produto_padrao(client)

    client.post("/carrinho/adicionar?usuario_id=1", json={
        "produto_id": 1,
        "quantidade": 3
    })

    resp = client.delete("/carrinho/limpar?usuario_id=1")
    assert resp.status_code == 200
    assert resp.json()["detail"] == "Carrinho vazio"

    # garantir que limpou
    carrinho = client.get("/carrinho/?usuario_id=1").json()
    assert carrinho["itens"] == []


def criar_produto_no_banco(db):
    produto = Produto(
        nome="Produto Teste",
        descricao="Descrição",
        preco=10.0,
        estoque=100
    )
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto


def test_adicionar_item_carrinho(client, db):
    produto = criar_produto_no_banco(db)

    response = client.post("/carrinho/adicionar", json={
        "usuario_id": 1,
        "produto_id": produto.id,
        "quantidade": 2
    })

    assert response.status_code == 200
    assert response.json()["mensagem"] == "Item adicionado ao carrinho"


def test_listar_itens_do_carrinho(client, db):
    produto = criar_produto_no_banco(db)

    # adiciona item
    client.post("/carrinho/adicionar", json={
        "usuario_id": 1,
        "produto_id": produto.id,
        "quantidade": 1
    })

    response = client.get("/carrinho/?usuario_id=1")
    assert response.status_code == 200
    assert len(response.json()["itens"]) == 1


def test_remover_item_carrinho(client, db):
    produto = criar_produto_no_banco(db)

    # adiciona item
    client.post("/carrinho/adicionar", json={
        "usuario_id": 1,
        "produto_id": produto.id,
        "quantidade": 1
    })

    # remove item
    response = client.delete("/carrinho/remover", json={
        "usuario_id": 1,
        "produto_id": produto.id
    })

    assert response.status_code == 200
    assert response.json()["mensagem"] == "Item removido do carrinho"
