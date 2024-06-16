import unittest
import os
import pandas as pd
from unittest.mock import patch
import sys

# Add the parent directory of the 'test' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Now you can import process_merged_GA from aggregate_ga
from Project.aggregate_g import process_merged_G

class TestGroupingAndAggregation(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_dir = os.path.join(current_dir, "test_data")
        
        os.makedirs(self.test_dir, exist_ok=True)
        
        self.csv_file_path = os.path.join(self.test_dir, "test_data.csv")
        test_data = """Artifact,Dependencies,artifact_release_date,dependency_release_date
group2:artifact1:1.0,group1:artifact1:1.0,2022-01-01,2023-01-01
group1:artifact2:1.0,group2:artifact2:1.0,2022-01-01,2022-01-01
group3:artifact2:1.0,group2:artifact2:1.0,2022-01-01,2022-01-01
"""
        with open(self.csv_file_path, "w") as f:
            f.write(test_data)
        
        os.makedirs(os.path.join(current_dir, "..", "project", "data"), exist_ok=True)
        
    def tearDown(self):
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)
        
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.figure')
    @patch('pandas.plotting._core.PlotAccessor.__call__')
    def test_grouping_and_aggregation(self, mock_plot, mock_figure, mock_show, mock_savefig):
        expected_data = {
            'Source_Group_Id': ["group1", "group2", "group2"],
            'Source Release Year': [2023, 2022, 2022],
            'Target_Group_Id': ["group2", "group1", "group3"],
            'Target Release Year': [2022, 2022, 2022],
            'Target_First_Release_Date': ["2022-01-01", "2022-01-01", "2022-01-01"],
            'Target_Last_Release_Date': ["2022-01-01", "2022-01-01", "2022-01-01"],
            'Target_Version_Count': [1, 1, 1],
            'Source_First_Release_Date': ["2023-01-01", "2022-01-01", "2022-01-01"],
            'Source_Last_Release_Date': ["2023-01-01", "2022-01-01", "2022-01-01"],
            'Source_Version_Count': [1, 1, 1]
        }
        
        expected_df = pd.DataFrame(expected_data)
        
        expected_df = expected_df.astype({
            'Source Release Year': 'int32',  
            'Target Release Year': 'int32',  
            'Target_First_Release_Date': 'object',
            'Target_Last_Release_Date': 'object',
            'Target_Version_Count': 'int64',
            'Source_First_Release_Date': 'object',
            'Source_Last_Release_Date': 'object',
            'Source_Version_Count': 'int64'
        })
        
        processed_df = process_merged_G(self.csv_file_path)
        
        processed_df['Source Release Year'] = processed_df['Source Release Year'].astype('int32')
        
        processed_df['Target Release Year'] = processed_df['Target Release Year'].astype('int32')

        expected_num_rows = 3
        self.assertEqual(len(processed_df), expected_num_rows)
        
        pd.testing.assert_frame_equal(processed_df, expected_df)

if __name__ == '__main__':
    unittest.main()
