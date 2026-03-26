# posto/pages/login.py
import streamlit as st
from posto.utils.drive import list_files

# Função para carregar arquivos do Drive
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

# Formulário de login
with st.form("login_form"):
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    submitted = st.form_submit_button("Entrar")

    if submitted:
        # Validação contra st.secrets
        auth = st.secrets["auth"]
        if username == auth["username"] and password == auth["password"]:
            st.session_state.logged_in = True
            st.session_state.arquivos = load_files()
            st.success("Login realizado com sucesso!")
        else:
            st.error("Usuário ou senha incorretos.")

# Mostra arquivos se logado
if st.session_state.logged_in:
    st.write("Arquivos disponíveis:")
    for f in st.session_state.arquivos:
        st.write(f"{f['name']} ({f['id']})")