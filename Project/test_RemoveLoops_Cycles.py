import unittest
import pandas as pd
from io import StringIO
from RemoveLoops_Cycles import clean_data

class TestCleanData(unittest.TestCase):

    def setUp(self):
        self.data_with_cycles_and_loops = StringIO("""source,target
A,B
B,A
C,C
D,E
E,D
F,G
""")
        self.expected_cleaned_data = pd.DataFrame({
            'source': ['A', 'D', 'F'],
            'target': ['B', 'E', 'G']
        })

    def test_clean_data(self):
        test_df = pd.read_csv(self.data_with_cycles_and_loops)
        test_df.to_csv('./data/test_links.csv', index=False)
        cleaned_df, cycle_error_count, loop_error_count = clean_data('./data/test_links.csv')

        pd.testing.assert_frame_equal(cleaned_df, self.expected_cleaned_data)
        self.assertEqual(cycle_error_count, 2)
        self.assertEqual(loop_error_count, 1)

if __name__ == '__main__':
    unittest.main()
