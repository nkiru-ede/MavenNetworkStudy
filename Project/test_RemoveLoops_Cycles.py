import pandas as pd
import networkx as nx
from io import StringIO

def test_cleaning_dataframe():
    csv_data = """
source,target
A,B
B,C
C,D
D,A
E,E
F,G
G,H
"""
    new_df = pd.read_csv(StringIO(csv_data), delimiter=',')
    new_df.columns = new_df.columns.str.replace('"', '').str.strip()

    dag = nx.DiGraph()
    cycle_error_count = 0
    loop_error_count = 0
    valid_rows = []

    for index, row in new_df.iterrows():
        source = row['source']
        target = row['target']

        if source == target:
            loop_error_count += 1
            continue

        dag.add_node(source)
        dag.add_node(target)

        if nx.has_path(dag, target, source):
            cycle_error_count += 1
            continue

        dag.add_edge(source, target)
        valid_rows.append(index)

    new_df_cleaned = new_df.loc[valid_rows].reset_index(drop=True)

   
    assert cycle_error_count == 1, f"Expected 1 cycle error, but found {cycle_error_count}."
    assert loop_error_count == 1, f"Expected 1 loop error, but found {loop_error_count}."
    assert len(new_df_cleaned) == 5, f"Expected cleaned DataFrame to have 5 rows, but found {len(new_df_cleaned)}."

    print("Test passed successfully.")

if __name__ == "__main__":
    test_cleaning_dataframe()
