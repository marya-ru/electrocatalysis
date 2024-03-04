import os
import pandas as pd
from src.utils import PATH_TO_DATA, PATH_TO_CALC_DATA


def load_dataset(path: str = os.path.join(PATH_TO_DATA, 'processed', 'data.csv')) -> pd.DataFrame:
    """
    Loads processed data
    :param path: processed data
    :return: processed DataFrame(pd.DataFrame)
    """

    data = pd.read_csv(path)
    return data


def load_raw_data(path: str = os.path.join(PATH_TO_DATA, 'experimental_data', 'data.xlsx')) -> pd.DataFrame:
    """
    Load raw experimental data
    :param path: raw experimental data
    :return: raw experimental DataFrame(pd.DataFrame)
    """
    data = pd.read_excel(path)
    data.drop(data.columns[0], axis=1, inplace=True)
    return data


def load_calc_data(path: str = PATH_TO_CALC_DATA) -> dict:

    data = {
        'R1': pd.read_excel(os.path.join(path, 'DFT_R1.xlsx')),
        'R2': pd.read_excel(os.path.join(path, 'DFT_R2.xlsx')),
        'LIGAND': pd.read_excel(os.path.join(path, 'DFT_LIGAND.xlsx')),
        'BASE': pd.read_excel(os.path.join(path, 'DFT_BASE.xlsx')),
        'SOLVENT': pd.read_excel(os.path.join(path, 'DFT_SOLV.xlsx')),
        'ELECTROLYTE': pd.read_excel(os.path.join(path, 'DFT_ELECTR.xlsx'))
    }

    return data
