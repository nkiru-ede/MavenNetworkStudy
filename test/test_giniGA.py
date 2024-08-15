import unittest
from unittest.mock import patch
import pandas as pd
import matplotlib.pyplot as plt
from gini_GA import analyze_gini_and_plot

class TestAnalyzeGiniAndPlot(unittest.TestCase):

    def setUp(self):
        self.test_file_path = './data/testdata_giniGA.csv'
        self.df = pd.read_csv(self.test_file_path)

    @patch('pandas.read_csv')
    def test_analyze_gini_and_plot(self, mock_read_csv):
        mock_read_csv.return_value = self.df

        with patch('matplotlib.pyplot.show'):
            analyze_gini_and_plot(self.test_file_path)

        expected_dependencies = ['A', 'B', 'C', 'D', 'E']
        expected_artifacts = ['F', 'G', 'H', 'I', 'J']
        
        self.df['Dependencies'] = self.df['Dependencies'].str.split(':').str[0]
        self.df['Artifact'] = self.df['Artifact'].str.split(':').str[0]
        
        self.assertTrue(all(self.df['Dependencies'].isin(expected_dependencies)))
        self.assertTrue(all(self.df['Artifact'].isin(expected_artifacts)))
        
        grouped = self.df.groupby(['Source Release Year', 'Dependencies']).size().reset_index(name='Count')
        self.assertEqual(len(grouped), 5) 

        
        
if __name__ == '__main__':
    unittest.main()
