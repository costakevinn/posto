import hashlib
import streamlit as st

def authenticate(username: str, password: str) -> bool:
    salt = st.secrets["auth"]["salt"]
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return (
        username == st.secrets["auth"]["username"]
        and password_hash == st.secrets["auth"]["password_hash"]
    )