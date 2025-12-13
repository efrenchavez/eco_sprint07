"""Offer functions to ease the access to the project's resources."""
from typing import Literal
import yaml

# constants
CONFIGURATION_FILE_NAME = 'config.yaml'

# load the configuration data from the YAML file
config_data = None
with open(CONFIGURATION_FILE_NAME, 'r', encoding='utf8') as config_file:
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
    print('----------------------------')
    print('*** Report End ***')
