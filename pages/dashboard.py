import streamlit as st

if not st.session_state.get("logged_in"):
    st.warning("Você precisa fazer login primeiro.")
    st.stop()

st.title("Dashboard")
st.info("Em breve.")