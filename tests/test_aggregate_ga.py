import unittest
import pandas as pd
from aggregate_ga import process_merged_GA

class TestGroupingAndAggregation(unittest.TestCase):
    def setUp(self):
        # Specify the file path to your test CSV file
        self.csv_file_path = "C:\\Users\\edenk\\Downloads\\test_data.csv"

    def test_grouping_and_aggregation(self):
        
        processed_df = process_merged_GA(self.csv_file_path)

       
        expected_num_rows = 2  

        
        self.assertEqual(len(processed_df), expected_num_rows)

if __name__ == '__main__':
    unittest.main()
