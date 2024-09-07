import unittest
import pandas as pd
from Project.TopnGAs import process_artifacts, get_top_10_per_year

class TestArtifactProcessing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Paths to the test CSV files
        cls.file_path = 'Project/data/gavTest.csv'
        cls.processed_df = process_artifacts(cls.file_path)

    def test_process_artifacts(self):
        # Define the expected output DataFrame
        expected_data = pd.DataFrame({
            'aggregated_artifact': ['ga1:foo', 'ga2:foo', 'ga1:foo', 'ga2:foo', 'ga3:foo'],
            'dependency_release_year': [2008, 2008, 2009, 2010, 2010],
            'dependency_count': [2, 1, 1, 1, 1]
        }).sort_values(by=['dependency_release_year', 'dependency_count'], ascending=[True, False]).reset_index(drop=True)
        
        # Ensure consistent data types
        expected_data['dependency_release_year'] = expected_data['dependency_release_year'].astype('int64')
        self.processed_df['dependency_release_year'] = self.processed_df['dependency_release_year'].astype('int64')
        
        # Assert the processed DataFrame matches the expected output
        pd.testing.assert_frame_equal(self.processed_df.reset_index(drop=True), expected_data)

    def test_get_top_10_per_year(self):
        # Call the function to get top 10 per year
        top_10 = get_top_10_per_year(self.processed_df)
        
        # Define the expected top 10 per year
        expected_top_10 = {
            2008: pd.DataFrame({
                'aggregated_artifact': ['ga1:foo', 'ga2:foo'],
                'dependency_release_year': [2008, 2008],
                'dependency_count': [2, 1]
            }).reset_index(drop=True),
            2009: pd.DataFrame({
                'aggregated_artifact': ['ga1:foo'],
                'dependency_release_year': [2009],
                'dependency_count': [1]
            }).reset_index(drop=True),
            2010: pd.DataFrame({
                'aggregated_artifact': ['ga2:foo', 'ga3:foo'],
                'dependency_release_year': [2010, 2010],
                'dependency_count': [1, 1]
            }).reset_index(drop=True)
        }
        
        # Ensure consistent data types
        for year, expected_df in expected_top_10.items():
            expected_df['dependency_release_year'] = expected_df['dependency_release_year'].astype('int64')
            top_10[year]['dependency_release_year'] = top_10[year]['dependency_release_year'].astype('int64')
            
            # Assert that the top 10 DataFrames match the expected DataFrames
            pd.testing.assert_frame_equal(top_10[year].reset_index(drop=True), expected_df)

if __name__ == '__main__':
    unittest.main()
