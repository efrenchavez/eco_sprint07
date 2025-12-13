"""Contains auxiliaries functions for use with the Jupyter notebook."""
import pandas as pd
def isna_report(aDataFrame: pd.DataFrame):
    rows = aDataFrame.shape[0]
    isna_sum = 0
    percentage = 0
    print('*** Missing/Null values report ***')
    print('----------------------------------')
    print()
    for column in aDataFrame:
        print(f'Examining column: \'{column}\'')
        isna_sum = aDataFrame[column].isna().sum()
        if 0 < isna_sum:
            print(f'NaN sum: {isna_sum}')
            percentage = round(isna_sum/rows*100, 4)
            print(f'Percentage: {percentage}')
        else:
            print('No missing values.')
        print()
    print('-----------------------------------')
    print('+++ Report END +++')


def check_info_in_decimals(aSeries: pd.Series):
    """Check if the decimal part of a Series of float contains information."""
    has_decimal_info = (aSeries % 1 != 0) & ~(aSeries.isna())
    return has_decimal_info.sum()
