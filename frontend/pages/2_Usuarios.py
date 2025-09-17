import streamlit as st
from utils.api import cadastrar_usuario, listar_usuarios
import requests

API_URL = "http://127.0.0.1:8000"

st.title("👤 Usuários")

# =========================
# 📌 Cadastro de Usuário + Endereço
# =========================
st.subheader("Cadastrar Novo Usuário")

col1, col2 = st.columns(2)

with col1:
    nome = st.text_input("Nome")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    telefone = st.text_input("Telefone")

with col2:
    st.markdown("**Endereço**")
    rua = st.text_input("Rua")
    cidade = st.text_input("Cidade")
    estado = st.text_input("Estado")
    cep = st.text_input("CEP")

if st.button("Cadastrar Usuário + Endereço"):
    if not (nome and email and senha and rua and cidade and estado and cep):
        st.warning("Preencha todos os campos obrigatórios.")
    else:
        # 1️⃣ Criar usuário
        resp_user = cadastrar_usuario(nome, email, senha, telefone)

        if resp_user.status_code in (200, 201):
            user = resp_user.json()
            st.success(f"Usuário {user['nome']} cadastrado com sucesso!")

            # 2️⃣ Criar endereço vinculado
            endereco = {
                "usuario_id": user["id"],
                "rua": rua,
                "cidade": cidade,
                "estado": estado,
                "cep": cep
            }
            resp_end = requests.post(f"{API_URL}/enderecos/", json=endereco)

            if resp_end.status_code in (200, 201):
                st.success("Endereço cadastrado com sucesso!")
            else:
                st.error(f"Erro ao cadastrar endereço: {resp_end.text}")

        else:
            st.error(f"Erro ao cadastrar usuário: {resp_user.text}")

# =========================
# 📌 Lista de Usuários
# =========================
st.subheader("Lista de Usuários")

usuarios = listar_usuarios()

if not usuarios:
    st.info("Nenhum usuário cadastrado.")
else:
    for u in usuarios:
        st.write(f"👤 **{u['nome']}** - {u['email']}")
        st.caption(f"📞 {u['telefone']}")
