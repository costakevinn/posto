# utils/auth.py
import streamlit as st
import hashlib

def check_password(password: str, salt: str, password_hash: str) -> bool:
    return hashlib.sha256((password + salt).encode()).hexdigest() == password_hash

def authenticate(username: str, password: str) -> bool:
    auth = st.secrets["auth"]
    return username == auth["username"] and check_password(password, auth["salt"], auth["password_hash"])

def require_login():
    """Interrompe a execução se o usuário não estiver logado"""
    if not st.session_state.get("logged_in", False):
        st.warning("Você precisa fazer login primeiro.")
        st.stop()