import streamlit as st
from utils.api import get

st.title("💳 Pagamentos")

pagamentos = get("/pagamentos/")

if "error" not in pagamentos:
    st.table(pagamentos)
else:
    st.error(pagamentos["error"])
