import unittest
import os
import pandas as pd
from aggregate_ga import process_merged_GA

class TestGroupingAndAggregation(unittest.TestCase):
    def setUp(self):
        # Specifying the file path to the test CSV file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.csv_file_path = os.path.join(current_dir, "data", "GAV", "test_data.csv")
        
         #check file path
        print("File path:", self.csv_file_path)

    def test_grouping_and_aggregation(self):
        expected_data = {
            'Source_Group_Id': ["group1", "group2", "group2"],
            'Source_Artifact_Id':["artifact1","artifact2", "artifact2"],
            'Source Release Date': ["1/01/2022", "1/01/2022","1/01/2022"],
            'Source Release Year': ["1/01", "1/01" ,"1/01" ],
            'Target_Group_Id': ["group2","group1","group3"],
            'Target_Artifact_Id':["artifact1","artifact2","artifact2"],
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
        
        processed_df = process_merged_GA(self.csv_file_path)
        
        expected_num_rows = 3
        self.assertEqual(len(processed_df), expected_num_rows)
        
        pd.testing.assert_frame_equal(processed_df, expected_df)
        
        #print(processed_df)
        #print(expected_df)

if __name__ == '__main__':
    unittest.main()
