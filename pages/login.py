import streamlit as st
from posto.utils.auth import authenticate
from posto.utils.drive import list_files

def load_files():
    try:
        return list_files(st.secrets["gdrive"]["folder_id"])
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
            st.success("Login realizado com sucesso!")
            st.experimental_rerun = None  # remove chamada antiga
        else:
            st.error("Usuário ou senha incorretos.")

# Mostra arquivos se logado
if st.session_state.logged_in:
    st.write("Arquivos disponíveis:")
    for f in st.session_state.arquivos:
        st.write(f"{f['name']} ({f.get('id', '')})")