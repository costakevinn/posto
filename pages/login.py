import streamlit as st
from utils.auth import authenticate
from utils.drive import list_files, download_file

def load_files():
    files = list_files()
    result = []
    for f in files:
        if f["mimeType"].startswith("application/vnd.google-apps"):
            continue
        data = download_file(f["id"])
        result.append({
            "name": f["name"],
            "data": data,
            "mime_type": f["mimeType"],
            "size": int(f.get("size", 0)),
        })
    return result

if st.session_state.get("authenticated"):
    st.switch_page("pages/arquivos.py")

st.title("RSLog")

username = st.text_input("Usuário")
password = st.text_input("Senha", type="password")

if st.button("Entrar", type="primary"):
    if authenticate(username, password):
        with st.spinner("Carregando arquivos..."):
            st.session_state.arquivos = load_files()
            st.session_state.authenticated = True
        st.switch_page("pages/arquivos.py")
    else:
        st.error("Usuário ou senha incorretos.")
