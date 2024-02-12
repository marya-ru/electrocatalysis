import streamlit as st
from src.utils import check_password


if not check_password():
    st.stop()

_, col2, _ = st.columns(3)

with col2:
    st.markdown("""
    ## Welcome page
    """)

st.markdown("""
### Introduction
...

### Reference
This project source code available in [repo](https://github.com/marya-ru/electrocatalysis)
""")
