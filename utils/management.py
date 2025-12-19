"""Offer functions to ease the access to the project's resources."""
from typing import Literal
import yaml
import pandas as pd

# constants
CONFIGURATION_FILE_NAME = 'config.yaml'
CONFIGURATION_FILE_NAME_FOR_MAIN = 'utils/config.yaml'

# load the configuration data from the YAML file
# if not running as __main__ assume main.py in project's root folder is executing
config_data = None
if __name__ == '__main__':
    with open(CONFIGURATION_FILE_NAME, 'r', encoding='utf8') as config_file:
        try:
            config_data = yaml.safe_load(config_file)
        except yaml.YAMLError as exc:
            print(exc)
else:
    with open(CONFIGURATION_FILE_NAME_FOR_MAIN, 'r', encoding='utf8') as config_file:
        try:
            config_data = yaml.safe_load(config_file)
        except yaml.YAMLError as exc:
            print(exc)


# functions


def get_path_to_data() -> Literal['data/', None]:
    """Construct the relative path of 'data/' for project's root."""
    result = None
    if config_data is not None:
        result = config_data['dataset']['path']
    return result


def get_path_to_csv_for_main() -> Literal['data/vehicles_us.csv', None]:
    """Construct the relative path of the dataset file for the app launcher."""
    result = None
    if config_data is not None:
        result = config_data['dataset']['path']
        result += config_data['dataset']['filename']
    return result


def get_path_to_clean_csv_for_main() -> Literal['data/clean_vehicles_us.csv', None]:
    """Construct the relative path of the clean dataset file for the app launcher."""
    result = None
    if config_data is not None:
        result = config_data['clean_dataset']['path']
        result += config_data['clean_dataset']['filename']
    return result


def get_path_to_dtypes_yaml_for_main() -> Literal['data/clean_vehicles_us_dtypes.yaml', None]:
    """Construct the relative path of the clean dataset dtypes yaml file for the app launcher."""
    result = None
    if config_data is not None:
        result = config_data['clean_dataset']['path']
        result += config_data['clean_dataset']['dtypes_yaml']
    return result


def get_path_to_csv_for_notebooks() -> Literal['../data/vehicles_us.csv', None]:
    """Construct the relative path of the dataset file for Jupyter Notebooks. """
    result = None
    if config_data is not None:
        result = '../'
        result += config_data['dataset']['path']
        result += config_data['dataset']['filename']
    return result


def get_path_to_notebooks() -> Literal['notebooks/', None]:
    """Construct the relative path to 'notebooks/' for project's root."""
    result = None
    if config_data is not None:
        result = config_data['notebooks']['path']
    return result


def get_path_to_utils() -> Literal['utils/', None]:
    """Construct the relative path to 'utils/' for project's root."""
    result = None
    if config_data is not None:
        result = config_data['utils']['path']
    return result


def load_clean_data_into_main() -> pd.DataFrame:
    """Build a dataframe using clean data."""
    result = pd.read_csv(get_path_to_clean_csv_for_main(), index_col=0)
    with open(get_path_to_dtypes_yaml_for_main(), 'r', encoding='utf8') as dtypes_file:
        try:
            dtypes_data = yaml.safe_load(dtypes_file)
        except yaml.YAMLError as exc:
            print(exc)
    column_dictionary = dtypes_data['columns']
    date_format = dtypes_data['date_format']
    for column_name, column_dtype in column_dictionary.items():
        if column_name == 'date_posted':
            result[column_name] = pd.to_datetime(
                result[column_name], format=date_format)
        else:
            result[column_name] = result[column_name].astype(column_dtype)
    return result


if __name__ == '__main__':
    print('*** Configuration report ***')
    print('----------------------------')
    print(f'Target YAML file: {CONFIGURATION_FILE_NAME}')
    print(f'YAML file read: {(config_data is not None)}')
    print('Dictionary retrieved:')
    print(config_data)
    print('Data folder:')
    print(f'\t{(get_path_to_data())}')
    print('Dataset path for app launcher:')
    print(f'\t{(get_path_to_csv_for_main())}')
    print('Dataset path for Jupyter Notebooks:')
    print(f'\t{(get_path_to_csv_for_notebooks())}')
    print('Jupyter notebooks folder:')
    print(f'\t{(get_path_to_notebooks())}')
    print('Utils library folder:')
    print(f'\t{(get_path_to_utils())}')
    print('Clean dataset path for app launcher:')
    print(f'\t{(get_path_to_clean_csv_for_main())}')
    print('Clean dataset\'s dytpe yaml path for app launcher:')
    print(f'\t{(get_path_to_dtypes_yaml_for_main())}')
    print('----------------------------')
    print('*** Report End ***')
