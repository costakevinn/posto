# app.py
import streamlit as st
from utils.auth import authenticate, require_login

# ---------- Inicializa session_state ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------- LOGIN ----------
if not st.session_state.logged_in:
    st.title("Login RSLog")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.success("Login realizado com sucesso!")
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos.")
    st.stop()  # bloqueia o restante do app até logar

# ---------- REQUER LOGIN ----------
require_login()

# ---------- PÁGINA PRINCIPAL: Arquivos ----------
st.title("Arquivos do projeto")

# Mock de arquivos
arquivos = [
    {"name": "arquivo1.pdf", "size": "2 MB"},
    {"name": "arquivo2.xlsx", "size": "5 MB"},
    {"name": "arquivo3.txt", "size": "1 MB"},
]

if not arquivos:
    st.info("Nenhum arquivo encontrado.")
else:
    st.caption(f"{len(arquivos)} arquivo(s)")
    for arq in arquivos:
        c1, c2, c3 = st.columns([5, 2, 2])
        with c1:
            st.write(arq["name"])
        with c2:
            st.caption(arq["size"])
        with c3:
            st.download_button(
                "⬇ Baixar",
                data=b"Arquivo de exemplo",
                file_name=arq["name"],
                mime="application/octet-stream",
                key=f"dl_{arq['name']}",
                use_container_width=True,
            )
        st.divider()

# ---------- LOGOUT ----------
if st.button("Sair"):
    st.session_state.clear()
    st.experimental_rerun()