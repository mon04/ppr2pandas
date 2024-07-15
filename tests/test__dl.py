import unittest
import logging
import io
from ppr2pandas._dl import download_ppr_all_csv, download_ppr_specific_csv


class TestDl(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger()

    def test_download_prr_all_csv(self):
        data = download_ppr_all_csv()
        self.assertTrue(len(data) > 0)
    
    def test_download_prr_all_csv(self):
        data = download_ppr_specific_csv("Carlow", 2011, 6)
        self.assertTrue(len(data) > 0)


if __name__ == '__main__':
    unittest.main()
