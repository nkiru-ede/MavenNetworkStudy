# -*- coding: utf-8 -*-
"""
Created on Sun May 26 19:22:19 2024

@author: edenk
"""

import unittest
import pandas as pd
import os
from aggregate_g import process_merged_G

class TestGroupingAndAggregation(unittest.TestCase):
    def setUp(self):
          
        # Specifying the file path to the test CSV file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.csv_file_path = os.path.join(current_dir, "data","GAV", "test_data.csv")
        

    def test_grouping_and_aggregation(self):
        expected_data = {
            'Source_Group_Id': ["group1", "group2", "group2"],
            'Source Release Date': ["1/01/2022", "1/01/2022","1/01/2022"],
            'Source Release Year': ["1/01", "1/01" ,"1/01" ],
            'Target_Group_Id': ["group2","group1","group3"],
            'Target Release Date': ["1/01/2023","1/01/2022","1/01/2022"],
            'Target Release Year': ["1/01","1/01","1/01"],
            'Target_First_Release_Date': ["1/01/2023","1/01/2022","1/01/2022"],
            'Target_Last_Release_Date': ["1/01/2023","1/01/2022","1/01/2022"],
            'Target_Version_Count': [1,1,1],
            'Source_First_Release_Date':["1/01/2022","1/01/2022","1/01/2022"],
            'Source_Last_Release_Date': ["1/01/2022","1/01/2022","1/01/2022"],
            'Source_Version_Count': [1,1,1]
            
        }
        expected_df = pd.DataFrame(expected_data)
        
        processed_df = process_merged_G(self.csv_file_path)

       
        expected_num_rows = 3  
        
        
        self.assertEqual(len(processed_df), expected_num_rows)
        pd.testing.assert_frame_equal(processed_df, expected_df)

if __name__ == '__main__':
    unittest.main()




