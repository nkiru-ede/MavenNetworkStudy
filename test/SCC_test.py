import unittest
import pandas as pd
#from SCC import collapse_sccs


from Project.SCC import collapse_sccs

class TestComputeSCCs(unittest.TestCase):

    def test_compute_sccs(self):
        links_data = """source,target
                        A,B
                        B,C
                        C,A
                        D,E
                        E,F
                        F,D
                        G,H"""
        release_data = """artifact,release
                          A,2024-01-01
                          B,2024-01-02
                          C,2024-01-03
                          D,2024-01-04
                          E,2024-01-05
                          F,2024-01-06
                          G,2024-01-07
                          H,2024-01-08"""

        links_df = pd.read_csv(pd.compat.StringIO(links_data), delimiter=',')
        release_df = pd.read_csv(pd.compat.StringIO(release_data), delimiter=',')

        result = collapse_sccs(links_df, release_df)
        
        # Expected strongly connected components
        expected_sccs = [{'A', 'B', 'C'}, {'D', 'E', 'F'}, {'G'}, {'H'}]
        result_sccs = [set(scc) for scc in result['sccs']]

        self.assertCountEqual(result_sccs, expected_sccs)
        self.assertEqual(result['max_scc_size'], 3)
        self.assertEqual(result['scc_sizes'], [3, 3, 1, 1])

if __name__ == "__main__":
    unittest.main()
