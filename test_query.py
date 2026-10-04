import streamlit as st

st.markdown('<a href="?page=test" target="_self">Click me</a>', unsafe_allow_html=True)

if st.query_params.get("page") == "test":
    st.write("Intercepted!")
    st.query_params.clear()
