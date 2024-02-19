import os
import streamlit as st
from src.utils import get_project_path
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

Electrochemical reaction yield depends on many parameters, primarily on the nature of the reactants, catalyst, solvent, electrolyte, etc., as well as on the parameters and type of current, concentration of substances, temperature, and synthesis time.

The traditional approach to finding optimal parameters experimentally requires a lot of time. Integrating machine learning can significantly speed up this process, while becoming a powerful tool for designing experiments to optimize synthesis conditions.

This project uses machine learning methods, experimental electrocatalysis data and DFT calculated data (homo energy, lumo energy, dipole moment) to predict NMR yield and the best parametrs of synthesis using regression models based on Scikit-learn.
""")

st.image(os.path.join(get_project_path(), 'images', 'workflow.png'))

st.markdown("""
### Reference
This project source code available in [repo](https://github.com/marya-ru/electrocatalysis)
""")
