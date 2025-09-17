import streamlit as st
from utils.api import cadastrar_produto

st.title("🆕 Cadastro de Produto")

nome = st.text_input("Nome do Produto")
descricao = st.text_area("Descrição")
preco = st.number_input("Preço (R$)", min_value=0.0, step=0.01, format="%.2f")
estoque = st.number_input("Estoque", min_value=0, step=1)

if st.button("Cadastrar Produto"):
    resp = cadastrar_produto(nome, descricao, preco, estoque)
    if resp.status_code in (200, 201):
        st.success("Produto cadastrado com sucesso!")
    else:
        st.error(f"Erro ao cadastrar produto: {resp.text}")
