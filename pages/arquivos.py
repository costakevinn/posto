import streamlit as st

# Protege a página: só acessível se logado
if not st.session_state.get("logged_in", False):
    st.warning("Você precisa fazer login primeiro.")
    st.stop()

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
                data=b"Conteúdo de exemplo",
                file_name=arq["name"],
                mime="application/octet-stream",
                key=f"dl_{arq['name']}",
                use_container_width=True,
            )
        st.divider()

if st.button("Sair"):
    st.session_state.clear()
    st.experimental_rerun()