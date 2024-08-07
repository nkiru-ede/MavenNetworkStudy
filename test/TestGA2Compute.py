import unittest
import pandas as pd

def compute_counts(df):
    df['dependency_release_date'] = pd.to_datetime(df['dependency_release_date'])
    df['artifact_release_date'] = pd.to_datetime(df['artifact_release_date'])

    earliest_dependency_dates = df.groupby('Dependencies')['dependency_release_date'].min().reset_index()
    earliest_artifact_dates = df.groupby('Artifact')['artifact_release_date'].min().reset_index()

    earliest_dependency_dates['Year'] = earliest_dependency_dates['dependency_release_date'].dt.year
    earliest_artifact_dates['Year'] = earliest_artifact_dates['artifact_release_date'].dt.year

    dependency_counts = earliest_dependency_dates.groupby('Year').size().reset_index(name='Count of Dependencies')
    artifact_counts = earliest_artifact_dates.groupby('Year').size().reset_index(name='Count of Artifacts')

    return dependency_counts, artifact_counts

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
