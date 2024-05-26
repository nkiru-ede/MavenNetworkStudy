# -*- coding: utf-8 -*-
"""
Created on Sun May 26 19:22:19 2024

@author: edenk
"""

import unittest
import pandas as pd
from aggregate_g import process_merged_G

class TestGroupingAndAggregation(unittest.TestCase):
    def setUp(self):
        # file path to the test data (this can be found in the data folder - 'test_data')
        self.csv_file_path = "C:\\Users\\edenk\\Downloads\\test_data.csv"

    def test_grouping_and_aggregation(self):
        
        processed_df = process_merged_G(self.csv_file_path)

       
        expected_num_rows = 3  

        
        self.assertEqual(len(processed_df), expected_num_rows)

if __name__ == '__main__':
    unittest.main()
