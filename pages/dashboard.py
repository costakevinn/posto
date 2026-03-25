import streamlit as st

if not st.session_state.get("authenticated"):
    st.switch_page("pages/login.py")

st.title("Dashboard")
st.info("Em breve.")
