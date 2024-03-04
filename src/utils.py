import os
import hmac
import pandas as pd
from pathlib import Path
import streamlit as st


def get_project_path() -> Path:
    """
    Reads path to the root of project
    :return: path(str) to root of project
    """
    return Path(__file__).parent.parent


PATH_TO_DATA = os.path.join(get_project_path(), 'data')
PATH_TO_MODELS = os.path.join(get_project_path(), 'models')
PATH_TO_REPORTS = os.path.join(get_project_path(), 'reports')
PATH_TO_PROCESSED_DATA = os.path.join(PATH_TO_DATA, 'processed', 'data.csv')

PATH_TO_CALC_DATA = os.path.join(PATH_TO_DATA, 'calculated_data')
PATH_TO_R1_CALC = os.path.join(PATH_TO_DATA, 'calculated_data', 'DFT_R1.xlsx')


MODELS = {
    'Linear regression': os.path.join(PATH_TO_MODELS, 'lr_pipeline.json'),
    'Random forest': os.path.join(PATH_TO_MODELS, 'RF_model.json'),
    'Gradient boosting': os.path.join(PATH_TO_MODELS, 'GBR_model.json')
}


def check_password():
    """Returns `True` if the user had a correct password."""
    if os.path.exists(os.path.join(get_project_path(), '.streamlit', 'secrets.toml')):
        def login_form():
            """Form with widget to collect user information"""
            with st.form("Credentials"):
                st.text_input("Username", key="username")
                st.text_input("Password", type='password', key='password')
                st.form_submit_button("Log in", on_click=password_entered)

        def password_entered():
            """Checks whether a password entered by the user is correct."""
            if st.session_state["username"] in st.secrets[
                "passwords"
            ] and hmac.compare_digest(
                st.session_state["password"],
                st.secrets.passwords[st.session_state["username"]],
            ):
                st.session_state["password_correct"] = True
                del st.session_state["password"]
                del st.session_state["username"]
            else:
                st.session_state["password_correct"] = False

        if st.session_state.get("password_correct", False):
            return True

        login_form()

        if "password_correct" in st.session_state:
            st.error("User not known or password incorrect")
        return False

    else:
        pass


def check_table(table):
    """
    Decode current type in table and reduce NMR Yield to from 0 to 100
    :param table: table with data
    :return: processed table with data
    """
    if table['NMR Yield (%)'] < 0:
        table['NMR Yield (%)'] = 0
    if table['NMR Yield (%)'] > 100:
        table['NMR Yield (%)'] = 100

    if table['Current type'] == 0:
        table['Current type'] = 'AC'
    else:
        table['Current type'] = 'DC'

    table = pd.DataFrame.from_dict(table, orient='index', columns=['Values'])
    return table
