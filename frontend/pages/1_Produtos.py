import streamlit as st
from utils.api import get

st.title("📦 Produtos disponíveis")

produtos = get("/produtos/")

if "error" not in produtos:
    for p in produtos:
        st.subheader(p["nome"])
        st.write(f"💰 Preço: R$ {p['preco']}")
        st.button(f"Adicionar {p['nome']} ao carrinho", key=p["id"])
else:
    st.error(produtos["error"])
