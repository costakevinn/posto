# app.py
import streamlit as st

# ---------- Funções de apoio ----------
def authenticate(username, password):
    """Valida usuário e senha"""
    # Aqui você pode substituir pelos seus dados reais ou conexão com banco
    return username == "rslog" and password == "123456"

def load_files():
    """Simula carregamento de arquivos"""
    # Aqui você pode colocar a lógica de pegar arquivos reais
    return [
        {"name": "arquivo1.pdf", "size": "2MB"},
        {"name": "arquivo2.xlsx", "size": "5MB"},
        {"name": "arquivo3.txt", "size": "1MB"},
    ]

# ---------- Inicializa estado ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "arquivos" not in st.session_state:
    st.session_state.arquivos = []

# ---------- Login ----------
if not st.session_state.logged_in:
    st.title("Login RSLog")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    login_btn = st.button("Entrar")

    if login_btn:
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.session_state.arquivos = load_files()
            st.success("Login realizado com sucesso!")
        else:
            st.error("Usuário ou senha incorretos.")

# ---------- Área logada ----------
if st.session_state.logged_in:
    st.title("Bem-vindo ao RSLog")
    st.write("Seus arquivos disponíveis:")
    for arquivo in st.session_state.arquivos:
        st.write(f"- {arquivo['name']} ({arquivo['size']})")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.arquivos = []
        st.success("Logout realizado com sucesso!")