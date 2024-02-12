import streamlit as st
from src.utils import check_password
from src.data.datasets import load_dataset, load_raw_data, load_calc_data

if not check_password():
    st.stop()


@st.cache_data
def load_all_data():
    """
    Loads in cache all data
    :return: 3 variables with data
    """
    raw_data_loaded = load_raw_data()
    processed_data_loaded = load_dataset()
    calc_data_loaded = load_calc_data()

    return raw_data_loaded, processed_data_loaded, calc_data_loaded


raw_data, processed_data, calc_data = load_all_data()

_, col2, _ = st.columns(3)

with col2:
    st.markdown("""
    ## All datasets
    """)

st.markdown("""
### Here you can see and download all datasets used in model fitting.
###### First one is raw data from experiment, you can download it by download button.
""")

_, col2, _ = st.columns(3)

with col2:
    st.download_button(label='Download raw data',
                       data=raw_data.to_csv(index=False).encode('utf-8'),
                       file_name='raw_data.csv',
                       mime='text/csv')


st.table(raw_data)

st.markdown("""
##### The second part is processed data. We encode all categorical values, calculate DFT and delete useless data
""")

_, col2, _ = st.columns(3)

with col2:
    st.download_button(label='Download processed data',
                       data=processed_data.to_csv(index=False).encode('utf-8'),
                       file_name='processed_data.csv',
                       mime='text/csv')

st.table(processed_data)

st.markdown("""
##### And the last one, all DFT calculation results
""")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.download_button(label='Download reagent 1 DFT data',
                       data=calc_data['R1'].to_csv(index=False).encode('utf-8'),
                       file_name='reagent_1_dft_data.csv',
                       mime='text/csv')

    st.table(calc_data['R1'])

with col2:
    st.download_button(label='Download reagent 2 DFT data',
                       data=calc_data['R2'].to_csv(index=False).encode('utf-8'),
                       file_name='reagent_2_dft_data.csv',
                       mime='text/csv')

    st.table(calc_data['R2'])

with col3:
    st.download_button(label='Download solvent DFT data',
                       data=calc_data['SOLVENT'].to_csv(index=False).encode('utf-8'),
                       file_name='solvent_dft_data.csv',
                       mime='text/csv')

    st.table(calc_data['SOLVENT'])

with col4:
    st.download_button(label='Download base DFT data',
                       data=calc_data['BASE'].to_csv(index=False).encode('utf-8'),
                       file_name='base_dft_data.csv',
                       mime='text/csv')

    st.table(calc_data['BASE'])

with col5:
    st.download_button(label='Download ligand DFT data',
                       data=calc_data['LIGAND'].to_csv(index=False).encode('utf-8'),
                       file_name='ligand_dft_data.csv',
                       mime='text/csv')

    st.table(calc_data['LIGAND'])

with col6:
    st.download_button(label='Download electrolyte DFT data',
                       data=calc_data['ELECTROLYTE'].to_csv(index=False).encode('utf-8'),
                       file_name='electrolyte_dft_data.csv',
                       mime='text/csv')

    st.table(calc_data['ELECTROLYTE'])
