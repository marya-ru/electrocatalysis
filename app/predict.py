import optuna
import numpy as np
import streamlit as st
from src.models.load_models import load_model
from src.models.model_predict import objective
from src.data.datasets import load_dataset, load_raw_data, load_calc_data
from src.utils import check_password, MODELS, PATH_TO_PROCESSED_DATA, check_table


#if not check_password():
    #st.stop()

st.set_page_config(
    layout='wide',
    initial_sidebar_state='expanded'
)

optuna.logging.set_verbosity(optuna.logging.WARNING)


@st.cache_resource
def load_data_and_model(path_to_data: str, model_name: str):
    """
    Loads data and model for prediction
    :param path_to_data: str to data
    :param model_name: Dict index in MODELS variable
    :return: (list) data variable(pd.DataFrame) and model variable
    """
    dataset = load_dataset(path_to_data)
    exp_dataset = load_raw_data()
    loaded_model = load_model(MODELS[model_name])
    return dataset, exp_dataset, loaded_model


@st.cache_data
def load_cache_calc():
    """
    Create cache with calc data
    :return: return cached calc data
    """
    return load_calc_data()


_, col2, _ = st.columns(3)
with col2:
    st.markdown("""
    ## Use model
    """)

st.markdown("""
### Here you can use model to predict optimal reaction parameters.

##### You need to select 2 reagents and start optimization.
""")

model_name_key = st.selectbox(
    'Select model',
    MODELS.keys(),
    index=2
)

data, exp_data, model = load_data_and_model(PATH_TO_PROCESSED_DATA, model_name_key)
calc_data = load_cache_calc()

st.markdown(
    """
    ### Select parameters
    #### Select reaction parameters
    """
)

reaction_type = st.selectbox(
    "Select reaction type",
    ["Amination",
     "Etherification",
     "Esterification"],
    index=0
)

new_params = st.checkbox('Set new DFT params')
new_input = None

if not new_params:
    new_input = None
    col1_input, col2_input = st.columns(2)

    with col1_input:
        reagent1 = st.selectbox(
            'Select Reagent 1',
            np.unique(exp_data['Reagent 1'].values)
        )

    with col2_input:
        reagent2 = st.selectbox(
            'Select Reagent 2',
            np.unique(exp_data['Reagent 2'].values)
        )

    st.markdown(
        """
        ##### DFT params of selected components
        """
    )

    col_reagent1, col_reagent2 = st.columns(2)

    with col_reagent1:
        st.write(f"{reagent1}")
        st.write(
            f"""
            Energy HOMO = `{calc_data['R1']['HOMO_R1'].loc[calc_data['R1']['Reagent 1'] == reagent1].values[0]}`
            """
        )

        st.write(
            f"""
            Energy LUMO = `{calc_data['R1']['LUMO_R1'].loc[calc_data['R1']['Reagent 1'] == reagent1].values[0]}`
            """
        )

        st.write(
            f"""
            Dipole moment = `{calc_data['R1']['MU_R1'].loc[calc_data['R1']['Reagent 1'] == reagent1].values[0]}`
            """
        )

    with col_reagent2:
        st.write(f"{reagent2}")
        st.write(
            f"""
            Energy HOMO = `{calc_data['R2']['HOMO_R2'].loc[calc_data['R2']['Reagent 2'] == reagent2].values[0]}`
            """
        )

        st.write(
            f"""
            Energy LUMO = `{calc_data['R2']['LUMO_R2'].loc[calc_data['R2']['Reagent 2'] == reagent2].values[0]}`
            """
        )

        st.write(
            f"""
            Dipole moment = `{calc_data['R2']['MU_R2'].loc[calc_data['R2']['Reagent 2'] == reagent2].values[0]}`
            """
        )

else:
    col1, col2 = st.columns(2)

    with col1:
        homo_r1 = st.number_input('Insert energy HOMO for reagent 1',
                                  value=0.0,
                                  max_value=100.0,
                                  min_value=-100.0,
                                  step=0.0001)

        lumo_r1 = st.number_input('Insert energy LUMO for reagent 1',
                                  value=0.0,
                                  max_value=100.0,
                                  min_value=-100.0,
                                  step=0.0001)

        mu_r1 = st.number_input('Insert dipole moment for reagent 1',
                                  value=0.0,
                                  max_value=100.0,
                                  min_value=-100.0,
                                  step=0.0001)

    with col2:
        homo_r2 = st.number_input('Insert energy HOMO for reagent 2',
                                  value=0.0,
                                  max_value=100.0,
                                  min_value=-100.0,
                                  step=0.0001)

        lumo_r2 = st.number_input('Insert energy LUMO for reagent 2',
                                  value=0.0,
                                  max_value=100.0,
                                  min_value=-100.0,
                                  step=0.0001)

        mu_r2 = st.number_input('Insert dipole moment for reagent 2',
                                  value=0.0,
                                  max_value=100.0,
                                  min_value=-100.0,
                                  step=0.0001)

    if homo_r1 == 0.0 and lumo_r1 == 0.0 and mu_r1 == 0.0:
        st.warning("Please insert params for reagent 1")
    elif homo_r2 == 0.0 and lumo_r2 == 0.0 and mu_r2 == 0.0:
        st.warning("Please insert params for reagent 2")
    else:
        new_input = [homo_r1, lumo_r1, mu_r1, homo_r2, lumo_r2, mu_r2]
        reagent1 = None
        reagent2 = None

st.markdown("""
### Prediction parameters
An optimization algorithm will be used to predict the best parameters. Specify the number of steps of the optimizer. The more steps, the longer the optimization will take.
""")

number_of_trials = st.number_input('Select number of optimization steps',
                                   value=100,
                                   min_value=2,
                                   max_value=10000,
                                   step=1)

if st.button('Predict NMR yield(%)'):
    study = optuna.create_study(direction='maximize')

    with st.spinner('Optimizing parameters...'):
        study.optimize(lambda trial: objective(trial, reagent1, reagent2, model, new_input, reaction_type=reaction_type), n_trials=number_of_trials)
    st.success('Done!')

    result_data = study.best_params
    result_data['NMR Yield (%)'] = round(study.best_trial.value, 2)

    result = check_table(result_data)

    st.table(result)
