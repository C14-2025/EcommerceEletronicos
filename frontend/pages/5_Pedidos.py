import streamlit as st
from utils.api import listar_usuarios, listar_produtos
import requests

API_URL = "http://127.0.0.1:8000"

st.title("📝 Pedidos")

# =========================
# 📌 Selecionar Usuário
# =========================
st.subheader("Selecionar Usuário")

usuarios = listar_usuarios()
if not usuarios:
    st.warning("Nenhum usuário cadastrado. Cadastre um primeiro.")
    st.stop()

usuarios_dict = {f"{u['nome']} ({u['email']})": u["id"] for u in usuarios}
usuario_escolhido = st.selectbox("Usuário:", list(usuarios_dict.keys()))

# =========================
# 📌 Selecionar Produtos
# =========================
st.subheader("Selecionar Produtos")

produtos = listar_produtos()
if not produtos:
    st.warning("Nenhum produto cadastrado. Cadastre um primeiro.")
    st.stop()

quantidades = {}
for p in produtos:
    qtd = st.number_input(
        f"{p['nome']} (R${p['preco']:.2f})",
        min_value=0,
        step=1,
        key=f"produto_{p['id']}"
    )
    if qtd > 0:
        quantidades[p['id']] = qtd

# =========================
# 📌 Criar Pedido
# =========================
if st.button("Criar Pedido"):
    if not quantidades:
        st.warning("Selecione pelo menos um produto.")
    else:
        pedido = {
            "usuario_id": usuarios_dict[usuario_escolhido],
            "endereco_id": 1,  # 👈 aqui simplificado: usa o primeiro endereço do usuário
            "itens": [{"produto_id": pid, "quantidade": qtd} for pid, qtd in quantidades.items()]
        }

        resp = requests.post(f"{API_URL}/pedidos/", json=pedido)

        if resp.status_code in (200, 201):
            st.success("Pedido criado com sucesso!")
            st.json(resp.json())  # mostra os dados retornados
        else:
            st.error(f"Erro ao criar pedido: {resp.text}")