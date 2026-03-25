import streamlit as st

if not st.session_state.get("authenticated"):
    st.switch_page("pages/login.py")

arquivos = st.session_state.get("arquivos", [])

col1, col2 = st.columns([8, 1])
with col1:
    st.title("Arquivos do projeto")
with col2:
    if st.button("Sair"):
        st.session_state.clear()
        st.switch_page("pages/login.py")

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
            kb = arq["size"] / 1024
            st.caption(f"{kb/1024:.1f} MB" if kb > 1024 else f"{kb:.0f} KB")
        with c3:
            st.download_button(
                "⬇ Baixar",
                data=arq["data"],
                file_name=arq["name"],
                mime=arq["mime_type"],
                key=f"dl_{arq['name']}",
                use_container_width=True,
            )
        st.divider()
