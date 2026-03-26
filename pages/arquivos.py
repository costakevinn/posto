import streamlit as st

if not st.session_state.get("logged_in"):
    st.warning("Você precisa fazer login primeiro.")
    st.stop()  # interrompe execução

arquivos = st.session_state.get("arquivos", [])

col1, col2 = st.columns([8, 1])
with col1:
    st.title("Arquivos do projeto")
with col2:
    if st.button("Sair"):
        st.session_state.clear()
        st.experimental_rerun = None  # remove experimental_rerun
        st.warning("Você saiu. Recarregue a página para logar novamente.")
        st.stop()

st.divider()

if not arquivos:
    st.info("Nenhum arquivo encontrado.")
else:
    st.caption(f"{len(arquivos)} arquivo(s)")
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