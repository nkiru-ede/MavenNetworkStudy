# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 16:46:03 2024

@author: edenk
"""

import os
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Sample data
links_data = {
    'source': ['A', 'B', 'C', 'D', 'E'],
    'target': ['B', 'C', 'A', 'E', 'F']
}

release_data = {
    'artifact': ['A', 'B', 'C', 'D', 'E', 'F'],
    'release': ['2024-01-01', '2023-06-15', '2022-12-31', '2023-09-20', '2024-02-10', '2023-11-05']
}


new_df = pd.DataFrame(links_data)
new_dataset = pd.DataFrame(release_data)

# Clean and merge data
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

new_df['dependency_release_date'] = pd.to_datetime(new_df['dependency_release_date'], format='%Y-%m-%d', errors='coerce')
new_df['artifact_release_date'] = pd.to_datetime(new_df['artifact_release_date'], format='%Y-%m-%d', errors='coerce')

# Create a directed graph (DAG)
dag = nx.DiGraph()

for _, row in new_df.iterrows():
    source = row['source']
    target = row['target']
    dag.add_edge(source, target)


sccs = list(nx.strongly_connected_components(dag))


scc_sizes = [len(scc) for scc in sccs]
scc_size_counts = pd.Series(scc_sizes).value_counts().sort_index()


scc_df = pd.DataFrame({
    'SCC Size': scc_size_counts.index,
    'Count': scc_size_counts.values
})


print(scc_df)


plt.figure(figsize=(10, 6))
plt.hist(scc_sizes, bins=range(1, max(scc_sizes) + 2), edgecolor='black')
plt.xlabel('Size of SCC')
plt.ylabel('Number of SCCs')
plt.title('Histogram of Strongly Connected Component Sizes')
plt.yscale('log') 
plt.grid(True)

plt.show()
