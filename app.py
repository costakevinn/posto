import streamlit as st

st.set_page_config(
    page_title="RSLog",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"Get Help": None, "Report a bug": None, "About": "RSLog App"},
)

# Inicializa estado
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Se não estiver logado, redireciona para login
if not st.session_state.logged_in:
    import pages.login  # importa a página de login
    st.stop()

# Se estiver logado, vai para a página de arquivos
import pages.arquivos  # importa a página de arquivos