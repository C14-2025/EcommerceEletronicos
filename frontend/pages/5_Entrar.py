import streamlit as st

st.title("🔑 Entrar")

opcao = st.radio("Escolha uma opção:", ["Login", "Cadastro"])

if opcao == "Login":
    usuario = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")
    if st.button("Fazer Login"):
        st.success(f"Bem-vindo, {usuario}!")

elif opcao == "Cadastro":
    novo_usuario = st.text_input("Nome Completo")
    cpf = st.text_input("CPF")
    nasc = st.text_input("Data de Nascimento")
    telefone = st.text_input("Telefone Celular:")
    email = st.text_input("E-mail")
    nova_senha = st.text_input("Crie sua senha", type="password")
    confirmar = st.text_input("Confirme sua Senha", type="password")
    
    if st.button("Cadastrar"):
        if nova_senha == confirmar:
            st.success(f"Usuário {novo_usuario} cadastrado com sucesso!")
        else:
            st.error("Senha incorreta")
