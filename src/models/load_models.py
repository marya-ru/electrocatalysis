import joblib


def load_model(path: str):
    """
    Loads scikit-learn model with joblib by path
    :param path: str to model
    :return: scikit-learn model
    """
    model = joblib.load(open(path, 'rb'))
    return model
