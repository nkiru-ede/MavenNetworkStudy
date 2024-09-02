import unittest
import pandas as pd
from Project.meanMedianGA import compute_statistics, load_and_process_data

class TestComputeStatistics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.all_ga_file_path = 'C:/Users/edenk/.spyder-py3/data/release_allTest.csv'
        cls.top_100_file_path = 'C:/Users/edenk/.spyder-py3/data/GA_test.csv'
        
        # Load and process test data
        cls.df_all_ga, cls.df_top_100 = load_and_process_data(cls.all_ga_file_path, cls.top_100_file_path)

    def test_compute_statistics(self):
        means_all, medians_all, means_top_100, medians_top_100 = compute_statistics(self.df_all_ga, self.df_top_100)

        # Expected results based on the test data
        expected_means_all = pd.DataFrame({
            'release_year': [2009, 2010, 2011],
            'mean_all': [0.125, 0.75, 0.125]
        })
        
        expected_medians_all = pd.DataFrame({
            'release_year': [2009, 2010, 2011],
            'median_all': [0.0, 1.0, 0.0]
        })

        expected_means_top_100 = pd.DataFrame({
            'release_year': [2009, 2010, 2011],
            'mean_top_100': [0.125, 0.75, 0.125] 
        })
        
        expected_medians_top_100 = pd.DataFrame({
            'release_year': [2009, 2010, 2011],
            'median_top_100': [0.0, 1.0, 0.0]  
        })

        try:
            pd.testing.assert_frame_equal(means_all, expected_means_all)
            pd.testing.assert_frame_equal(medians_all, expected_medians_all)
            pd.testing.assert_frame_equal(means_top_100, expected_means_top_100)
            pd.testing.assert_frame_equal(medians_top_100, expected_medians_top_100)
        except AssertionError as e:
            print(f"AssertionError: {e}")
            raise

if __name__ == '__main__':
    unittest.main()
