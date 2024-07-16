import requests
import zipfile
import io
from string import Template

"""
This module is used internally to download data from the PPR website.
"""

# https://docs.python.org/2/library/codecs.html#standard-encodings
_PPR_ENCODING = 'cp1252'

_ALL_URL = (
    "https://www.propertypriceregister.ie/website/npsra/ppr/"
    "npsra-ppr.nsf/Downloads/PPR-ALL.zip/$FILE/PPR-ALL.zip")

_SPECIFIC_URL_TEMPLATE = Template(
    "https://www.propertypriceregister.ie/website/npsra/ppr/"
    "npsra-ppr.nsf/Downloads/PPR-$year-$month-$county.csv/"
    "$$FILE/PPR-$year-$month-$county.csv")


def download_ppr_all_csv():
    """
    Download the entire PPR as a CSV-formatted string.
    
    Returns
    -------
    str
        The entire PPR in CSV format.
    """
    response = requests.get(_ALL_URL, verify=False)
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as the_zip:
            file_name = the_zip.namelist()[0]
            with the_zip.open(file_name) as file:
                return file.read().decode(_PPR_ENCODING)
    else:
        raise Exception(
            f"Failed to download file: status code {response.status_code}")


def download_ppr_specific_csv(county: str, year: int, month: int) -> str:
    """
    Download specific PPR data for a given county, year, and month as a 
    CSV-formatted string.
    
    Parameters
    ----------
    county : str 
        The name of the county.
    year : int
        The year of the data.
    month : int
        The month of the data (1-12).
    
    Returns
    -------
    str
        The selected PPR data in CSV format.
    """
    print("Template", _SPECIFIC_URL_TEMPLATE.template)
    url = _SPECIFIC_URL_TEMPLATE.substitute({
            'year': year, 
            'month': f"{month:02d}", 
            'county': county
        })
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.content.decode(_PPR_ENCODING)
    else:
        raise Exception(
            f"Failed to download file: status code {response.status_code}")
