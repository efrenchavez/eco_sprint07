"""Contains auxiliaries functions for use with the Jupyter notebook: EDA.ipynb"""
import pandas as pd
import numpy as np
import itertools as it

# Missing Values Auxiliary Functions


def isna_report(aDataFrame: pd.DataFrame) -> None:
    """
    Print to console a report of columns containing missing values.

    First, output single column analysis, indicating missing value count & which percentage of rows contain missing values.
    Then, do the same for 2, 3, ..., n combinations of columns.
    """

    rows = aDataFrame.shape[0]
    isna_sum = 0
    percentage = 0
    print('*** Missing/Null values report ***')
    print('----------------------------------')
    if aDataFrame.isna().any(axis=1).any(axis=0):
        print('Single column analysis')
        print()
        columns_with_nas = []
        for column in aDataFrame:
            isna_sum = aDataFrame[column].isna().sum()
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
                isna_sum = aDataFrame[list(
                    combination)].isna().all(axis=1).sum()
                percentage = round(isna_sum/rows*100, 1)
                print(
                    f'{isna_sum} ({percentage}%) concurrent missing values in: {combination}')
            print()
    else:
        print('No missing values found.')
    print('-----------------------------------')
    print('+++ Report END +++')


def row_by_row_fix_paint_color_nas(aDataFrameRow: pd.Series, model_col: str, color_col: str, aDictionary: dict) -> pd.Series:
    """If the row constains a missing value in color, fill it with the color mode from the dictionary using model as key."""
    result = aDataFrameRow.copy()
    if str(result[color_col]) == 'nan':
        result[color_col] = aDictionary[result[model_col]]
    return result


def fix_paint_color_nas(aDataFrame: pd.DataFrame, model_col: str, color_col: str) -> pd.DataFrame:
    """Fill missing values in vehicle color with that vehicle's model's color mode."""
    modes = aDataFrame.groupby(model_col)[color_col].agg(
        lambda x: list(pd.Series.mode(x))[0] if 0 < len(list(pd.Series.mode(x))) else np.nan)
    # turn series into a dictionary so we can access the color mode using 'model' as key
    modes = modes.to_dict()
    result = aDataFrame.copy()
    result = result.apply(lambda row: row_by_row_fix_paint_color_nas(
        row, model_col, color_col, modes), axis=1)
    return result


def row_by_row_fix_odometer_nas(aDataFrameRow: pd.Series, condition_col: str, odometer_col: str, aDictionary: dict) -> pd.Series:
    """If the row constains a missing value in odometer, fill it with the odometer mean from the dictionary using condition as key."""
    result = aDataFrameRow.copy()
    if str(result[odometer_col]) == 'nan':
        result[odometer_col] = aDictionary[result[condition_col]]
    return result


def fix_odometer_nas(aDataFrame: pd.DataFrame, condition_col: str, odometer_col: str) -> pd.DataFrame:
    """Fill missing values in odometer with that vehicle's condition's mean."""
    means = aDataFrame.groupby(condition_col)[odometer_col].mean()
    means = means.to_dict()
    result = aDataFrame.copy()
    result = result.apply(lambda row: row_by_row_fix_odometer_nas(
        row, condition_col, odometer_col, means), axis=1)
    return result


def fix_nas(aDataFrame: pd.DataFrame, four_wd_col: str = 'is_4wd', model_year_col: str = 'model_year', cylinders_col: str = 'cylinders',
            model_col: str = 'model', color_col: str = 'paint_color', condition_col: str = 'condition', odometer_col: str = 'odometer') -> pd.DataFrame:
    """Fix all missing values in the dataframe."""
    result = aDataFrame.copy()
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


def check_info_in_decimals(aSeries: pd.Series) -> bool:
    """Check if the decimal part of a Series of float contains information."""
    # this creates a boolean mask where the series is neither na nor divisible by 1, then sums it
    result = ((aSeries % 1 != 0) & ~(aSeries.isna())).sum()
    # is the previous sum greater than 0?
    result = 0 < result
    return result


def fix_data_for_a_category(aDataFrameColumn: pd.Series, column_name: str) -> pd.Series:
    """Turn a column into a category, log process to console."""
    print(f'Fitting data type for column: \'{column_name}\'')
    print(f'\tcardinality: {aDataFrameColumn.nunique()}')
    print('\tdue to context as category, casting to \'category\'')
    return aDataFrameColumn.astype('category')


def fix_data_types(aDataFrame: pd.DataFrame, price_col: str = 'price', year_col: str = 'model_year', model_col: str = 'model',
                   condition_col: str = 'condition', cylinders_col: str = 'cylinders', fuel_col: str = 'fuel', odometer_col: str = 'odometer',
                   transmission_col: str = 'transmission', type_col: str = 'type', color_col: str = 'paint_color', data_col: str = 'date_posted',
                   days_col: str = 'days_listed') -> pd.DataFrame:
    """Fix the data types of the dataframe to better suit its context and contents."""
    result = aDataFrame.copy()
    # Fix price
    print(f'Fitting data type for column: \'{price_col}\'')
    print(
        f'\tmin: {result[price_col].min()}\tmax: {result[price_col].max()}')
    print(f'\trequires negative values?: {(result[price_col].min() < 0)}')
    print('\tdue to monetary context, casting to \'float32\'')
    result[price_col] = result[price_col].astype('float32')
    # Fix year
    print(f'Fitting data type for column: \'{year_col}\'')
    print(
        f'\tmin: {result[year_col].min()}\tmax: {result[year_col].max()}')
    print(f'\trequires negative values?: {(result[year_col].min() < 0)}')
    print(
        f'\trequires decimal part?: {check_info_in_decimals(result[year_col])}')
    print('\tdue to context as year, casting to \'uint16\'')
    result[year_col] = result[year_col].astype('uint16')
    # Fix model
    result[model_col] = fix_data_for_a_category(result[model_col], model_col)
    # Fix condition
    result[condition_col] = fix_data_for_a_category(
        result[condition_col], condition_col)
    # Fix cylinders
    print(f'Fitting data type for column: \'{cylinders_col}\'')
    print(
        f'\tmin: {result[cylinders_col].min()}\tmax: {result[cylinders_col].max()}')
    print(f'\trequires negative values?: {(result[cylinders_col].min() < 0)}')
    print(
        f'\trequires decimal part?: {check_info_in_decimals(result[cylinders_col])}')
    print('\tdue to context as a whole positive number, casting to \'uint8\'')
    result[cylinders_col] = result[cylinders_col].astype('uint8')
    # Fix fuel
    result[fuel_col] = fix_data_for_a_category(result[fuel_col], fuel_col)
    # Fix odometer
    print(f'Fitting data type for column: \'{odometer_col}\'')
    print(
        f'\tmin: {result[odometer_col].min()}\tmax: {result[odometer_col].max()}')
    print(f'\trequires negative values?: {(result[odometer_col].min() < 0)}')
    print(
        f'\trequires decimal part?: {check_info_in_decimals(result[odometer_col])}')
    print('\tdue to context as a fractional value, casting to \'float32\'')
    result[odometer_col] = result[odometer_col].astype('float32')
    # Fix transmission
    result[transmission_col] = fix_data_for_a_category(
        result[transmission_col], transmission_col)
    # Fix type
    result[type_col] = fix_data_for_a_category(result[type_col], type_col)
    # Fix color
    result[color_col] = fix_data_for_a_category(result[color_col], color_col)
    return result
