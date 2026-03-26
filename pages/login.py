import streamlit as st
from utils.auth import authenticate

st.title("Login RSLog")

username = st.text_input("Usuário")
password = st.text_input("Senha", type="password")
login_clicked = st.button("Entrar")

if login_clicked:
    if authenticate(username, password):
        st.session_state.logged_in = True
        st.success("Login realizado com sucesso!")
        st.experimental_rerun()  # recarrega o app já logado
    else:
        st.error("Usuário ou senha incorretos.")

st.stop()  # impede que outra página seja carregada antes do login