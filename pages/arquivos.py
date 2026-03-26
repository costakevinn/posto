# pages/arquivos.py
import streamlit as st
from utils.auth import require_login

require_login()  # garante que só usuários logados acessam

arquivos = st.session_state.get("arquivos", [])

st.title("Arquivos do projeto")
if not arquivos:
    st.info("Nenhum arquivo encontrado.")
else:
    for arq in arquivos:
        st.write(f"- {arq['name']} ({arq['size']/1024:.1f} KB)")