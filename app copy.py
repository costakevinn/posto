import streamlit as st
import sys
import os

# Adiciona a raiz ao sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.auth import authenticate
from utils.drive import list_files

# ----------------------------
# Inicializa session_state
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "arquivos" not in st.session_state:
    st.session_state.arquivos = []

# ----------------------------
# Funções
# ----------------------------
def load_files():
    try:
        files = list_files(st.secrets["gdrive"]["folder_id"])
        return files
    except Exception as e:
        st.error(f"Erro ao listar arquivos: {e}")
        return []

def logout():
    st.session_state.clear()
    st.experimental_rerun()

# ----------------------------
# Layout
# ----------------------------
st.set_page_config(page_title="RSLog", page_icon="📁", layout="wide")

if not st.session_state.logged_in:
    # Tela de login
    st.title("Login RSLog")
    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar")
        if submitted:
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.arquivos = load_files()
                st.success("Login realizado com sucesso!")
                st.experimental_rerun()
            else:
                st.error("Usuário ou senha incorretos.")
else:
    # ----------------------------
    # Tabs (apenas após login)
    # ----------------------------
    st.sidebar.button("Sair", on_click=logout)

    tabs = ["Arquivos", "Dashboard", "Relatórios"]
    selected_tab = st.tabs(tabs)

    # Arquivos
    with selected_tab[0]:
        st.header("Arquivos do projeto")
        arquivos = st.session_state.arquivos
        if not arquivos:
            st.info("Nenhum arquivo encontrado.")
        else:
            for arq in arquivos:
                c1, c2, c3 = st.columns([5, 2, 2])
                with c1:
                    st.write(arq["name"])
                with c2:
                    size_kb = arq.get("size", 0) / 1024
                    st.caption(f"{size_kb/1024:.1f} MB" if size_kb > 1024 else f"{size_kb:.0f} KB")
                with c3:
                    st.download_button(
                        "⬇ Baixar",
                        data=arq.get("data", b""),
                        file_name=arq["name"],
                        mime=arq.get("mimeType", "application/octet-stream"),
                        key=f"dl_{arq['name']}",
                        use_container_width=True,
                    )
                st.divider()

    # Dashboard
    with selected_tab[1]:
        st.header("Dashboard")
        st.info("Em breve.")

    # Relatórios
    with selected_tab[2]:
        st.header("Relatórios")
        st.info("Em breve.")