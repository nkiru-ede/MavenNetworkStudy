# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 15:24:11 2024

@author: edenk
"""

import pandas as pd
import os
import networkx as nx

def clean_data(links_file):
    new_df = pd.read_csv(links_file, delimiter=',')
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

    return new_df_cleaned, cycle_error_count, loop_error_count

if __name__ == "__main__":
    data_folder = './data'
    links_file = os.path.join(data_folder, 'links_all.csv')

    new_df_cleaned, cycle_error_count, loop_error_count = clean_data(links_file)

    print("Cycle errors adding edges:", cycle_error_count)
    print("Loop errors adding edges:", loop_error_count)
    print("Length of cleaned DataFrame:", len(new_df_cleaned))

    # Save cleaned DataFrame for Part 2 and Part 3
    new_df_cleaned.to_csv('./data/cleaned_data.csv', index=False)
