import streamlit as st

st.set_page_config(page_title="RSLog", page_icon="📁", layout="wide")

# Inicializa estado de autenticação
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.switch_page("pages/login.py")
else:
    st.switch_page("pages/arquivos.py")