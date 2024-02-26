import numpy as np
import pandas as pd
from src.data.datasets import load_dataset, load_calc_data


def objective(trial, reagent_1: str, reagent_2: str, model, new_input: list = None, reaction_type: str = "Amination"):
    """
    Create optimization objective to select best params for NMR Yield increase
    :param trial: Optuna object
    :param reagent_1: First selected reagent(str)
    :param reagent_2: Second selected reagent(str)
    :param model: Scikit-learn fitted model
    :param new_input: List with homo, lumo, mu for reagent 1 and reagent 2
    :return:
    """
    data = load_dataset()
    calc_data = load_calc_data()

    if new_input is None:
        homo_r1 = [calc_data['R1']['HOMO_R1'].loc[calc_data['R1']['Reagent 1'] == reagent_1].values[0]]
        lumo_r1 = [calc_data['R1']['LUMO_R1'].loc[calc_data['R1']['Reagent 1'] == reagent_1].values[0]]
        mu_r1 = [calc_data['R1']['MU_R1'].loc[calc_data['R1']['Reagent 1'] == reagent_1].values[0]]
        homo_r2 = [calc_data['R2']['HOMO_R2'].loc[calc_data['R2']['Reagent 2'] == reagent_2].values[0]]
        lumo_r2 = [calc_data['R2']['LUMO_R2'].loc[calc_data['R2']['Reagent 2'] == reagent_2].values[0]]
        mu_r2 = [calc_data['R2']['MU_R2'].loc[calc_data['R2']['Reagent 2'] == reagent_2].values[0]]
    else:
        homo_r1, lumo_r1, mu_r1, homo_r2, lumo_r2, mu_r2 = new_input

    amount_ligand = trial.suggest_categorical('Amount of ligand (mol %)', np.unique(data['Amount of ligand (mol %)']).tolist())
    amount_base = trial.suggest_categorical('Amount of base (eq.)', np.unique(data['Amount of base (eq.)']).tolist())
    frequency = trial.suggest_categorical('Frequency (Hz)', np.unique(data['Frequency (Hz)']).tolist())
    temperature = trial.suggest_categorical('Temperature(C)', np.unique(data['Temperature(C)']).tolist())
    reaction_time = trial.suggest_categorical('Time (h)', np.unique(data['Time (h)']).tolist())
    current_type = trial.suggest_categorical('Current type', np.unique(data['Current type']).tolist())
    solv = trial.suggest_categorical('solvent', np.unique(calc_data['SOLVENT']['Solvent']).tolist())
    if reaction_type == "Amination":
        base = trial.suggest_categorical('base', ['-'])
    else:
        base_iter = np.unique(calc_data['BASE']['Base']).tolist()
        base_iter.remove('-')
        base = trial.suggest_categorical('base', base_iter)

    ligand_iter = np.unique(calc_data['LIGAND']['Ligand']).tolist()
    ligand_iter.remove('-')
    ligand = trial.suggest_categorical('ligand', ligand_iter)
    electrolyte = trial.suggest_categorical('electrolyte', np.unique(calc_data['ELECTROLYTE']['Electrolyte']).tolist())

    input_data = pd.DataFrame(data={
        'Amount of ligand (mol %)': [amount_ligand],
        'Amount of base (eq.)': [amount_base],
        'Frequency (Hz)': [frequency],
        'Temperature(C)': [temperature],
        'Time (h)': [reaction_time],
        'Current type': [current_type],
        'HOMO_R1': homo_r1,
        'LUMO_R1': lumo_r1,
        'MU_R1': mu_r1,
        'HOMO_R2': homo_r2,
        'LUMO_R2': lumo_r2,
        'MU_R2': mu_r2,
        'HOMO_SOLV': [calc_data['SOLVENT']['HOMO_SOLV'].loc[calc_data['SOLVENT']['Solvent'] == solv].values[0]],
        'LUMO_SOLV': [calc_data['SOLVENT']['LUMO_SOLV'].loc[calc_data['SOLVENT']['Solvent'] == solv].values[0]],
        'MU_SOLV': [calc_data['SOLVENT']['MU_SOLV'].loc[calc_data['SOLVENT']['Solvent'] == solv].values[0]],
        'HOMO_BASE': [calc_data['BASE']['HOMO_BASE'].loc[calc_data['BASE']['Base'] == base].values[0]],
        'LUMO_BASE': [calc_data['BASE']['LUMO_BASE'].loc[calc_data['BASE']['Base'] == base].values[0]],
        'MU_BASE': [calc_data['BASE']['MU_BASE'].loc[calc_data['BASE']['Base'] == base].values[0]],
        'HOMO_LIGAND': [calc_data['LIGAND']['HOMO_LIGAND'].loc[calc_data['LIGAND']['Ligand'] == ligand].values[0]],
        'LUMO_LIGAND': [calc_data['LIGAND']['LUMO_LIGAND'].loc[calc_data['LIGAND']['Ligand'] == ligand].values[0]],
        'MU_LIGAND': [calc_data['LIGAND']['MU_LIGAND'].loc[calc_data['LIGAND']['Ligand'] == ligand].values[0]],
        'HOMO_ELECTR': [calc_data['ELECTROLYTE']['HOMO_ELECTR'].loc[calc_data['ELECTROLYTE']['Electrolyte'] == electrolyte].values[0]],
        'LUMO_ELECTR': [
            calc_data['ELECTROLYTE']['LUMO_ELECTR'].loc[calc_data['ELECTROLYTE']['Electrolyte'] == electrolyte].values[
                0]],
        'MU_ELECTR': [
            calc_data['ELECTROLYTE']['MU_ELECTR'].loc[calc_data['ELECTROLYTE']['Electrolyte'] == electrolyte].values[
                0]],
    })

    pred = model.predict(input_data)
    return pred
