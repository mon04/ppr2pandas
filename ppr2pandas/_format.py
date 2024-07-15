import pandas as pd
from pandas import DataFrame
import io
from datetime import datetime
from typing import List

"""
This module is used internally for data processing and formatting.
"""

# PPR column names
_DATE_COL             = 'Date of Sale (dd/mm/yyyy)'
_ADDRESS_COL          = 'Address'
_COUNTY_COL           = 'County'
_EIRCODE_COL          = 'Eircode'
_PRICE_COL            = 'Price (€)'
_NOT_FULL_MKT_PRC_COL = 'Not Full Market Price'
_VAT_EXCL_COL         = 'VAT Exclusive'
_DESCRIPTION_COL      = 'Description of Property'
_SIZE_COL             = 'Property Size Description'

# PPR column order
_COLUMNS = [
    _DATE_COL,
    _ADDRESS_COL, 
    _COUNTY_COL, 
    _EIRCODE_COL, 
    _PRICE_COL, 
    _NOT_FULL_MKT_PRC_COL, 
    _VAT_EXCL_COL, 
    _DESCRIPTION_COL, 
    _SIZE_COL,
]


def parse_csv(csv: str) -> DataFrame:
    """
    Converts CSV-formatted PPR data to a pandas DataFrame object.

    Parameters
    ----------
    csv : str
        The CSV-formatted PPR data.
    """
    df = pd.read_csv(io.StringIO(csv), header=0, dtype=str, usecols=_COLUMNS)

    # parse dates
    df[_DATE_COL] = pd.to_datetime(df[_DATE_COL], format="%d/%m/%Y")

    # parse prices
    df[_PRICE_COL] = (
        df[_PRICE_COL]
         .replace('€', '', regex=True)
         .replace(',', '', regex=True)
         .astype(float))
    
    # parse bools i.e. "Yes"/"No" columns
    for col in [_NOT_FULL_MKT_PRC_COL, _VAT_EXCL_COL]:
        df[col] = df[col].map({'Yes': True, 'No': False})
    
    return df


def filter(df: DataFrame, min_date: datetime = None, max_date: datetime = None, 
           min_price: float = None, max_price: float = None, 
           counties: List[str] = None) -> DataFrame:
    """
    Filter the PPR data based on the provided criteria.

    Parameters
    ----------
    df : DataFrame
        The parsed PPR dataset.
    min_date : datetime.datetime, optional
        Minimum date of sale for the data.
    max_date : datetime.datetime, optional
        Maximum date of sale for the data.
    min_price : float, optional
        Minimum price for the data.
    max_price : float, optional
        Maximum price for the data.
    counties : list | str, optional
        Match only data from these counties.

    Returns
    -------
    DataFrame
        The filtered PPR dataset.
    """
    if min_date:
        df = df[df[_DATE_COL] >= min_date]

    if max_date:
        df = df[df[_DATE_COL] <= max_date]
    
    if min_price:
        df = df[df[_PRICE_COL] >= min_price]

    if max_price:
        df = df[df[_PRICE_COL] <= max_price]
    
    if type(counties) == list:
        counties = [county.lower() for county in counties]
        df = df[df['County'].str.lower().isin(counties)]

    return df.reset_index(drop=True)
