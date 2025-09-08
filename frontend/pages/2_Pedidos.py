import streamlit as st
from utils.api import get

st.title("📝 Pedidos")

pedidos = get("/pedidos/")

if "error" not in pedidos:
    st.table(pedidos)
else:
    st.error(pedidos["error"])
