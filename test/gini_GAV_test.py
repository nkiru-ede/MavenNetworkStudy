import unittest
from Project.gini_GAV import calculate_gini_from_csv  

class TestGiniCalculation(unittest.TestCase):

    def test_calculate_gini_from_csv(self):
        # Path to the test CSV file
        file_path = 'Project/data/gavTest.csv'

        gini_per_year = calculate_gini_from_csv(file_path)

        # Expected Gini coefficients based on the test CSV data
        expected_gini_per_year = {
            2008: 0.0,  
            2009: 0.0,  
            2010: 0.0   
        }

        # Assert Gini coefficients, allowing for floating-point imprecision
        for year, expected_gini in expected_gini_per_year.items():
            self.assertAlmostEqual(gini_per_year.get(year, 0.0), expected_gini, places=6,
                                   msg=f"Gini coefficient for year {year} doesn't match.")

if __name__ == '__main__':
    unittest.main()
