# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 14:36:21 2024

@author: edenk
"""

import pandas as pd
import os
import networkx as nx
import matplotlib.pyplot as plt

# Load data
data_folder = './data'
links_file = os.path.join(data_folder, 'links_all.csv')
release_file = os.path.join(data_folder, 'release_all.csv')

new_df = pd.read_csv(links_file, delimiter=',')
new_dataset = pd.read_csv(release_file, delimiter=',')

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

new_df['dependency_release_date'] = pd.to_datetime(new_df['dependency_release_date'], format='ISO8601', errors='coerce')
new_df['artifact_release_date'] = pd.to_datetime(new_df['artifact_release_date'], format='ISO8601', errors='coerce')

dag = nx.DiGraph()

cycle_error_count = 0
loop_error_count = 0
missing_timestamp_count = 0

for _, row in new_df.iterrows():
    source = row['source']
    target = row['target']
    dependency_date = row['dependency_release_date']
    artifact_date = row['artifact_release_date']

    if pd.isna(dependency_date) or pd.isna(artifact_date):
        print(f"Missing timestamp for {source} or {target}")
        missing_timestamp_count += 1
        continue

    if source == target:
        print(f"Loop detected: {source} -> {target}")
        loop_error_count += 1
        continue

    dag.add_node(source)
    dag.add_node(target)

    if nx.has_path(dag, target, source):
        print(f"Cycle detected: adding edge {source} -> {target} would create a cycle")
        cycle_error_count += 1
        continue

    dag.add_edge(source, target)

vertex_count = len(dag.nodes)
edge_count = len(dag.edges)

print("Cycle errors adding edges:", cycle_error_count)
print("Loop errors adding edges:", loop_error_count)
print("Missing timestamp errors:", missing_timestamp_count)
print("Vertex count:", vertex_count)
print("Edge count:", edge_count)

sccs = list(nx.strongly_connected_components(dag))

scc_sizes = [len(scc) for scc in sccs]

max_scc_size = max(scc_sizes) if scc_sizes else 0

max_sccs = [scc for scc in sccs if len(scc) == max_scc_size]

print(f"Number of maximum size SCCs: {len(max_sccs)}")
for idx, scc in enumerate(max_sccs):
    print(f"Max SCC {idx + 1} (size {max_scc_size}): {scc}")

# Plot histogram of maximum SCC sizes
plt.hist([max_scc_size] * len(max_sccs), bins=range(1, max_scc_size + 2), edgecolor='black')
plt.xlabel('Size of SCC')
plt.ylabel('Number of SCCs')
plt.title('Histogram of Maximum Size Strongly Connected Components')
plt.show()
