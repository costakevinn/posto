import streamlit as st
from utils.auth import authenticate, require_login
from utils.drive import list_files

# ---------- Inicializa session_state ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "arquivos" not in st.session_state:
    st.session_state.arquivos = []

# ---------- Login ----------
if not st.session_state.logged_in:
    st.title("Login RSLog")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.session_state.arquivos = list_files(st.secrets["gdrive"]["folder_id"])
            st.experimental_rerun()  # reinicia o app
        else:
            st.error("Usuário ou senha incorretos.")
    st.stop()  # bloqueia o restante do app