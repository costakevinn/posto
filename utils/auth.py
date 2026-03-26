# posto/utils/auth.py
import hashlib
import streamlit as st

def authenticate(username: str, password: str) -> bool:
    """Verifica usuário e senha usando st.secrets com salt + hash"""
    salt = st.secrets["auth"]["salt"]
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return (
        username == st.secrets["auth"]["username"]
        and password_hash == st.secrets["auth"]["password_hash"]
    )

def require_login():
    """Interrompe execução se usuário não estiver logado"""
    if not st.session_state.get("logged_in"):
        st.warning("Você precisa fazer login primeiro.")
        st.stop()