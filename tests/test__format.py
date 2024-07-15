import unittest
import pandas as pd
from datetime import datetime
from pandas.testing import assert_frame_equal
from ppr2pandas._format import parse_csv, filter
import numpy as np


_DATE_COL             = 'Date of Sale (dd/mm/yyyy)'
_ADDRESS_COL          = 'Address'
_COUNTY_COL           = 'County'
_EIRCODE_COL          = 'Eircode'
_PRICE_COL            = 'Price (€)'
_NOT_FULL_MKT_PRC_COL = 'Not Full Market Price'
_VAT_EXCL_COL         = 'VAT Exclusive'
_DESCRIPTION_COL      = 'Description of Property'
_SIZE_COL             = 'Property Size Description'


class TestFormatModule(unittest.TestCase):

    def setUp(self):
        self.csv_data = (
            'Date of Sale (dd/mm/yyyy),Address,County,Eircode,Price (€),Not Full Market Price,VAT Exclusive,Description of Property,Property Size Description\n'
            '"01/06/2011","33 BROWNSHILL WOOD, CARLOW","Carlow","","€230,000.00","No","No","Second-Hand Dwelling house /Apartment",""\n'
            '"02/06/2011","60 DUBLIN ROAD, TULLOW","Carlow","","€48,000.00","No","No","Second-Hand Dwelling house /Apartment",""\n'
            '"02/06/2011","Bohermore, Bagenalstown","Carlow","","€235,000.00","No","Yes","Second-Hand Dwelling house /Apartment",""\n'
            '"02/06/2011","Cherry Trees, Castlemore, Tullow","Carlow","","€90,000.00","Yes","No","Second-Hand Dwelling house /Apartment",""\n'
            '"03/06/2011","19 Old Burrin, Burrin Road, Carlow","Carlow","","€145,000.00","Yes","No","Second-Hand Dwelling house /Apartment",""\n'
        )
        self.df = parse_csv(self.csv_data)

    def test_parse_csv(self):
        expected_data = {
            _DATE_COL: [
                datetime(2011, 6, 1), datetime(2011, 6, 2), 
                datetime(2011, 6, 2), datetime(2011, 6, 2), 
                datetime(2011, 6, 3), 
            ],
            _ADDRESS_COL: [
                '33 BROWNSHILL WOOD, CARLOW', 
                '60 DUBLIN ROAD, TULLOW', 
                'Bohermore, Bagenalstown', 
                'Cherry Trees, Castlemore, Tullow', 
                '19 Old Burrin, Burrin Road, Carlow'
            ],
            _COUNTY_COL: ['Carlow'] * 5,
            _EIRCODE_COL: [None] * 5,
            _PRICE_COL: [230000.0, 48000.0, 235000.0, 90000.0, 145000.0],
            _NOT_FULL_MKT_PRC_COL: [False, False, False, True, True],
            _VAT_EXCL_COL: [False, False, True, False, False],
            _DESCRIPTION_COL: [
                'Second-Hand Dwelling house /Apartment'] * 5,
            _SIZE_COL: [None] * 5
        }
        expected_df = pd.DataFrame(expected_data)
        assert_frame_equal(self.df, expected_df)

    def test_filter_min_date(self):
        min_date = datetime(2011, 6, 2)
        filtered_df = filter(self.df, min_date=min_date)
        expected_df = (
            self.df[self.df[_DATE_COL] >= min_date]
             .reset_index(drop=True))
        assert_frame_equal(filtered_df, expected_df)

    def test_filter_max_date(self):
        max_date = datetime(2011, 6, 2)
        filtered_df = filter(self.df, max_date=max_date)
        expected_df = (
            self.df[self.df[_DATE_COL] <= max_date]
             .reset_index(drop=True))
        assert_frame_equal(filtered_df, expected_df)

    def test_filter_min_price(self):
        min_price = 90000.0
        filtered_df = filter(self.df, min_price=min_price)
        expected_df = (
            self.df[self.df[_PRICE_COL] >= min_price].reset_index(drop=True))
        assert_frame_equal(filtered_df, expected_df)

    def test_filter_max_price(self):
        max_price = 90000.0
        filtered_df = filter(self.df, max_price=max_price)
        expected_df = (
            self.df[self.df[_PRICE_COL] <= max_price].reset_index(drop=True))
        assert_frame_equal(filtered_df, expected_df)

    def test_filter_counties(self):
        counties = ['Carlow']
        filtered_df = filter(self.df, counties=counties)
        expected_df = (
            self.df[
                self.df[_COUNTY_COL].str.lower()
                 .isin([county.lower() for county in counties])
            ].reset_index(drop=True))
        assert_frame_equal(filtered_df, expected_df)


if __name__ == '__main__':
    unittest.main()
