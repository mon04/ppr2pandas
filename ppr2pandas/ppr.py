from pandas import DataFrame
from datetime import datetime
from typing import List
from _dl import download_ppr_all_csv
from _format import parse_csv, filter


def get_ppr(min_date: datetime = None, max_date: datetime = None, 
            min_price: float = None, max_price: float = None, 
            counties: List[str] = None) -> DataFrame:
    """
    Download PPR data as a DataFrame.

    Parameters
    ----------
    min_date : datetime.datetime, optional 
        Minimum date of sale for the data.
    max_date : datetime.datetime, optional 
        Maximim date of sale for the data.
    min_price : float, optional 
        Minimum price for the data.
    max_price : float, optional 
        Maximum price for the data.
    counties : List[str], optional 
        Match only data from these counties.
    
    Returns
    -------
    DataFrame
        The PPR data requested.
    """
    csv = download_ppr_all_csv()
    return filter(parse_csv(csv), min_date=min_date, max_date=max_date,
                  min_price=min_price, max_price=max_price, counties=counties)
