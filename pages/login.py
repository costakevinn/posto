import streamlit as st
import sys
import os

# Adiciona a raiz do projeto ao sys.path para encontrar utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.auth import authenticate
from utils.drive import list_files

def load_files():
    try:
        files = list_files(st.secrets["gdrive"]["folder_id"])
        return files
    except Exception as e:
        st.error(f"Erro ao listar arquivos: {e}")
        return []

# Inicializa session_state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "arquivos" not in st.session_state:
    st.session_state.arquivos = []

with st.form("login_form"):
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    submitted = st.form_submit_button("Entrar")

    if submitted:
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.session_state.arquivos = load_files()
            st.session_state.authenticated = True
            st.success("Login realizado com sucesso!")
        else:
            st.error("Usuário ou senha incorretos.")

if st.session_state.logged_in:
    st.write("Arquivos disponíveis:")
    for f in st.session_state.arquivos:
        st.write(f"{f['name']} ({f.get('id', '')})")