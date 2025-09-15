import streamlit as st

st.set_page_config(page_title="Ecommerce de Peças", layout="wide")

col1, col2, col3 = st.columns([6, 1, 1])  

with col3:
    
    if st.button("Entrar"):
        st.switch_page("pages/Entrar.py")  

st.title("🖥️ Electronic Ecommerce")
st.write("Bem-vindo ao sistema de Ecommerce!")
st.write("Navegue pelas páginas laterais para visualizar produtos, pedidos, pagamentos e usuários.")