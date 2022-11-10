import os

def data_root() -> str:
    """
    Return the root path to the stock cases
    """

    dir_name = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.normpath(os.path.join(dir_name, '..', '..', 'datasets'))
    return data_path

def get_data(data_name) -> str:
    """
    Return the path to the stock cases

    Parameters
    ----------
    data_name : str
        Name of the data, such as 'sourcedata/sample.csv'
    """
    return data_root() + '/' + data_name
