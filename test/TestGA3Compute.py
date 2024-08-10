# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 20:12:01 2024

@author: edenk
"""

import unittest
import pandas as pd
from ComputeGA3 import compute_counts_GA3

class TestComputeCounts(unittest.TestCase):
    
    def setUp(self):
        self.df = pd.read_csv('./data/test_data.csv')

    def test_compute_counts(self):
        dependency_counts, artifact_counts = compute_counts_GA3(self.df)
        

        # Expected results
        expected_dependency_counts = pd.DataFrame({
            'Year': [2011, 2012, 2013],
            'Count of Dependencies': [1, 1, 1]
        })

        expected_artifact_counts = pd.DataFrame({
            'Year': [2011],
            'Count of Artifacts': [3]
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
