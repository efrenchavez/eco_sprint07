"""Contains auxiliaries functions for use with the Jupyter notebook: EDA.ipynb"""
import yaml
import pandas as pd
import numpy as np
import itertools as it

# Missing Values Auxiliary Functions


def isna_report(a_data_frame: pd.DataFrame) -> None:
    """
    Print to console a report of columns containing missing values.

    First, output single column analysis, indicating missing value count & which percentage of rows contain missing values.
    Then, do the same for 2, 3, ..., n combinations of columns.
    """

    rows = a_data_frame.shape[0]
    isna_sum = 0
    percentage = 0
    print('*** Missing/Null values report ***')
    print('----------------------------------')
    if a_data_frame.isna().any(axis=1).any(axis=0):
        print('Single column analysis')
        print()
        columns_with_nas = []
        for column in a_data_frame:
            isna_sum = a_data_frame[column].isna().sum()
            if 0 < isna_sum:
                columns_with_nas.append(column)
                percentage = round(isna_sum/rows*100, 1)
                print(
                    f'{isna_sum} ({percentage}%) missing values in column: \'{column}\'')
        print()
        for i in range(2, len(columns_with_nas)+1):
            print(f'Multiple column analysis ({i})')
            print()
            combinations = it.combinations(columns_with_nas, i)
            for combination in combinations:
                isna_sum = a_data_frame[list(
                    combination)].isna().all(axis=1).sum()
                percentage = round(isna_sum/rows*100, 1)
                print(
                    f'{isna_sum} ({percentage}%) concurrent missing values in: {combination}')
            print()
    else:
        print('No missing values found.')
    print('-----------------------------------')
    print('+++ Report END +++')


def row_by_row_fix_paint_color_nas(a_data_frame_row: pd.Series, model_col: str, color_col: str, aDictionary: dict) -> pd.Series:
    """If the row constains a missing value in color, fill it with the color mode from the dictionary using model as key."""
    result = a_data_frame_row.copy()
    if str(result[color_col]) == 'nan':
        result[color_col] = aDictionary[result[model_col]]
    return result


def fix_paint_color_nas(a_data_frame: pd.DataFrame, model_col: str, color_col: str) -> pd.DataFrame:
    """Fill missing values in vehicle color with that vehicle's model's color mode."""
    modes = a_data_frame.groupby(model_col)[color_col].agg(
        lambda x: list(pd.Series.mode(x))[0] if 0 < len(list(pd.Series.mode(x))) else np.nan)
    # turn series into a dictionary so we can access the color mode using 'model' as key
    modes = modes.to_dict()
    result = a_data_frame.copy()
    result = result.apply(lambda row: row_by_row_fix_paint_color_nas(
        row, model_col, color_col, modes), axis=1)
    return result


def row_by_row_fix_odometer_nas(a_data_frame_row: pd.Series, condition_col: str, odometer_col: str, aDictionary: dict) -> pd.Series:
    """If the row constains a missing value in odometer, fill it with the odometer mean from the dictionary using condition as key."""
    result = a_data_frame_row.copy()
    if str(result[odometer_col]) == 'nan':
        result[odometer_col] = aDictionary[result[condition_col]]
    return result


def fix_odometer_nas(a_data_frame: pd.DataFrame, condition_col: str, odometer_col: str) -> pd.DataFrame:
    """Fill missing values in odometer with that vehicle's condition's mean."""
    means = a_data_frame.groupby(condition_col)[odometer_col].mean()
    means = means.to_dict()
    result = a_data_frame.copy()
    result = result.apply(lambda row: row_by_row_fix_odometer_nas(
        row, condition_col, odometer_col, means), axis=1)
    return result


def fix_nas(a_data_frame: pd.DataFrame, four_wd_col: str = 'is_4wd', model_year_col: str = 'model_year', cylinders_col: str = 'cylinders',
            model_col: str = 'model', color_col: str = 'paint_color', condition_col: str = 'condition', odometer_col: str = 'odometer') -> pd.DataFrame:
    """Fix all missing values in the dataframe."""
    result = a_data_frame.copy()
    original_rows, original_columns = result.shape
    print('*** Fixing missing values ***')
    print('-----------------------------')
    print(f'Dropping column: \'{four_wd_col}\'...')
    result = result.drop(four_wd_col, axis=1)
    print(
        f'Dropping rows with missing values from \'{model_year_col}\' and \'{cylinders_col}\'...')
    result = result.dropna(subset=[model_year_col, cylinders_col])
    print(f'Inputting values for \'{color_col}\'...')
    result = fix_paint_color_nas(result, model_col, color_col)
    print(f'Inputting values for \'{odometer_col}\'...')
    result = fix_odometer_nas(result, condition_col, odometer_col)
    # calculate % of rows lost
    final_rows, final_columns = result.shape
    lost_rows = original_rows - final_rows
    lost_columns = original_columns - final_columns
    percentage_rows = round(lost_rows/original_rows*100, 1)
    percentage_columns = round(lost_columns/original_columns*100, 1)
    print(
        f'Starting rows: {original_rows} Rows after: {final_rows} ({lost_rows} rows lost, {percentage_rows}%)')
    print(
        f'Starting columns: {original_columns} Columns after: {final_columns} ({lost_columns} columns lost, {percentage_columns}%)')
    print('-----------------------------')
    print('+++ Missing values FIXED +++')
    return result

# Data types auxiliary functions


def check_info_in_decimals(a_data_frame_column: pd.Series) -> bool:
    """Check if the decimal part of a Series of float contains information."""
    # this creates a boolean mask where the series is neither na nor divisible by 1, then sums it
    result = ((a_data_frame_column % 1 != 0) & ~
              (a_data_frame_column.isna())).sum()
    # is the previous sum greater than 0?
    result = 0 < result
    return result


def fix_data_for_a_category(a_data_frame: pd.DataFrame, column_name: str) -> pd.Series:
    """Turn a column into a category, log process to console."""
    print(f'Fitting data type for column: \'{column_name}\'')
    print(f'\tcardinality: {a_data_frame[column_name].nunique()}')
    print('\tdue to context as category, casting to \'category\'')
    return a_data_frame[column_name].astype('category')


def print_data_for_numeric(a_data_frame: pd.DataFrame, column_name: str) -> None:
    """Print to console the repetitive text used in the process of fixing dtypes for numeric variables."""
    print(f'Fitting data type for column: \'{column_name}\'')
    print(
        f'\tmin: {a_data_frame[column_name].min()}\tmax: {a_data_frame[column_name].max()}')
    print(
        f'\trequires negative values?: {(a_data_frame[column_name].min() < 0)}')
    print(
        f'\trequires decimal part?: {check_info_in_decimals(a_data_frame[column_name])}')


def fix_data_types(a_data_frame: pd.DataFrame, price_col: str = 'price', year_col: str = 'model_year', model_col: str = 'model',
                   condition_col: str = 'condition', cylinders_col: str = 'cylinders', fuel_col: str = 'fuel', odometer_col: str = 'odometer',
                   transmission_col: str = 'transmission', type_col: str = 'type', color_col: str = 'paint_color', date_col: str = 'date_posted',
                   days_col: str = 'days_listed') -> pd.DataFrame:
    """Fix the data types of the dataframe to better suit its context and contents."""
    result = a_data_frame.copy()
    # there are no ordinal categoricals, so I can jam all the categorical conversion in one for loop
    # since they don't require custom processing or output
    categorical_columns = [model_col, condition_col,
                           fuel_col, transmission_col, type_col, color_col]
    for categorical_column in categorical_columns:
        # Fix each categorical columns
        result[categorical_column] = fix_data_for_a_category(
            result, categorical_column)

    # different numeric columns require specialized processing and output
    # they will be fixed one by one
    # Fix price
    print_data_for_numeric(result, price_col)
    print('\tdue to monetary context, casting to \'float32\'')
    result[price_col] = result[price_col].astype('float32')
    # Fix year
    print_data_for_numeric(result, year_col)
    print('\tdue to context as year, casting to \'uint16\'')
    result[year_col] = result[year_col].astype('uint16')
    # Fix cylinders
    print_data_for_numeric(result, cylinders_col)
    print('\tdue to context as a whole positive number, casting to \'uint8\'')
    result[cylinders_col] = result[cylinders_col].astype('uint8')
    # Fix odometer
    print_data_for_numeric(result, odometer_col)
    print('\tdue to context as a fractional value, casting to \'float32\'')
    result[odometer_col] = result[odometer_col].astype('float32')
    # Fix days listed
    print_data_for_numeric(result, days_col)
    print('\tdue to context as whole days, casting to \'uint16\'')
    result[days_col] = result[days_col].astype('uint16')

    # fixing the date column
    print(f'Fitting data type for column: \'{date_col}\'')
    print('\tdue to context as datetime, casting to \'datetime64[ns]\'')
    result[date_col] = pd.to_datetime(result[date_col], format='%Y-%m-%d')
    return result


def export_clean_data(a_data_frame: pd.DataFrame, full_path_to_csv_file: str, full_path_to_yaml_file) -> None:
    """Write clean data to a csv and data type dict to a YAML"""
    print(f'Exporting dataframe to file: \'{full_path_to_csv_file}\'')
    try:
        a_data_frame.to_csv(full_path_to_csv_file)
        print(f'\t{full_path_to_csv_file} created successfully.')
    except FileNotFoundError:
        print(f'Error creating file: {full_path_to_csv_file}')
    except:
        print('Error saving clean data to file.')
    print('Creating data types correction dictionary...')
    # now create the YAML
    # .dtypes gets me a series,
    # apply will get me only the names of the dtypes,
    # to dict will make it a directory
    dtype_dictionary = a_data_frame.dtypes.apply(lambda x: x.name).to_dict()
    output_dictionary = {}
    output_columns = {}
    for column, type in dtype_dictionary.items():
        print(f'\tcolumn: \'{column}\', is of type: \'{type}\'')
        output_columns[column] = type
    output_dictionary = {'columns': output_columns}
    print('Datetime format for the only date column is \'%Y-%m-%d\'')
    output_dictionary['date_format'] = '%Y-%m-%d'
    print('Output dictionary preview:')
    print(output_dictionary)
    # save to file
    with open(full_path_to_yaml_file, 'w') as file:
        yaml.dump(output_dictionary, file, default_flow_style=False, indent=2)
