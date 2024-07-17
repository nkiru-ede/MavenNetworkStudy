# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 14:36:21 2024

@author: edenk
"""

import pandas as pd
import os
import networkx as nx
import matplotlib.pyplot as plt

def compute_sccs(data_folder='./data'):
    links_file = os.path.join(data_folder, 'links_all.csv')
    release_file = os.path.join(data_folder, 'release_all.csv')

    new_df = pd.read_csv(links_file, delimiter=',')
    new_dataset = pd.read_csv(release_file, delimiter=',')

    new_df.columns = new_df.columns.str.replace('"', '').str.strip()
    new_dataset.columns = new_dataset.columns.str.replace('"', '').str.strip()

    new_df = new_df.merge(new_dataset[['artifact', 'release']], how='left', left_on='source', right_on='artifact')
    new_df.rename(columns={'release': 'dependency_release_date'}, inplace=True)
    new_df.drop(columns=['artifact'], inplace=True)

    new_df = new_df.merge(new_dataset[['artifact', 'release']], how='left', left_on='target', right_on='artifact')
    new_df.rename(columns={'release': 'artifact_release_date'}, inplace=True)
    new_df.drop(columns=['artifact'], inplace=True)

    new_df['dependency_release_date'] = new_df['dependency_release_date'].str.replace(r'\[GMT\]', '', regex=True)
    new_df['artifact_release_date'] = new_df['artifact_release_date'].str.replace(r'\[GMT\]', '', regex=True)

    new_df['dependency_release_date'] = pd.to_datetime(new_df['dependency_release_date'], format='ISO8601', errors='coerce')
    new_df['artifact_release_date'] = pd.to_datetime(new_df['artifact_release_date'], format='ISO8601', errors='coerce')

    dag = nx.DiGraph()

    for _, row in new_df.iterrows():
        source = row['source']
        target = row['target']

        if source != target:
            dag.add_edge(source, target)

    sccs = list(nx.strongly_connected_components(dag))
    scc_sizes = [len(scc) for scc in sccs]
    max_scc_size = max(scc_sizes) if scc_sizes else 0
    max_sccs = [scc for scc in sccs if len(scc) == max_scc_size]

    plt.hist(scc_sizes, bins=range(1, max(scc_sizes, default=0) + 2), edgecolor='black')
    plt.xlabel('Size of SCC')
    plt.ylabel('Number of SCCs')
    plt.title('Histogram of Strongly Connected Components Sizes')
    plt.show()

    return {
        "sccs": sccs,
        "scc_sizes": scc_sizes,
        "max_scc_size": max_scc_size,
        "max_sccs": max_sccs
    }

if __name__ == "__main__":
    data_folder = './data'
    compute_sccs(data_folder)
