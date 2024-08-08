import unittest
import pandas as pd
from ComputeGA2 import compute_counts

class TestComputeCounts(unittest.TestCase):
    
    def setUp(self):
        self.df = pd.read_csv('./data/test_data.csv')

    def test_compute_counts(self):
        dependency_counts, artifact_counts = compute_counts(self.df)

        # Expected results
        expected_dependency_counts = pd.DataFrame({
            'Year': [2011, 2012, 2013],
            'Count of Dependencies': [1, 1, 1]
        })

        expected_artifact_counts = pd.DataFrame({
            'Year': [2009, 2010],
            'Count of Artifacts': [2, 1]
        })

        dependency_counts['Year'] = dependency_counts['Year'].astype('int64')
        artifact_counts['Year'] = artifact_counts['Year'].astype('int64')
        expected_dependency_counts['Year'] = expected_dependency_counts['Year'].astype('int64')
        expected_artifact_counts['Year'] = expected_artifact_counts['Year'].astype('int64')

        # Assert the results
        pd.testing.assert_frame_equal(dependency_counts, expected_dependency_counts)
        pd.testing.assert_frame_equal(artifact_counts, expected_artifact_counts)

if __name__ == '__main__':
    unittest.main()
