import streamlit as st
from utils.api import get

st.title("👤 Usuários")

usuarios = get("/usuarios/")

if "error" not in usuarios:
    for u in usuarios:
        st.write(f"ID: {u['id']} - Nome: {u['nome']}")
else:
    st.error(usuarios["error"])
