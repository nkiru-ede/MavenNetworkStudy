# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 18:01:11 2024

@author: edenk
"""

import pandas as pd
import os
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

data_folder = './data'
links_file = os.path.join(data_folder, 'transitive_dependencies.csv')
release_file = os.path.join(data_folder, 'release_all.csv')

# Read the CSV file with error handling
def read_csv_file(file_path, expected_columns):
    valid_rows = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if len(row) == expected_columns:
                valid_rows.append(row)
            else:
                print(f"Skipping malformed line {i + 1}: {row}")
    return pd.DataFrame(valid_rows, columns=['source', 'target'])


new_df = read_csv_file(links_file, 2)


new_dataset = pd.read_csv(release_file, delimiter=',')
new_dataset.columns = new_dataset.columns.str.replace('"', '').str.strip()

new_df.columns = new_df.columns.str.replace('"', '').str.strip()


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

new_dataset['release'] = new_dataset['release'].str.replace(r'\[GMT\]', '', regex=True)
new_dataset['release'] = pd.to_datetime(new_dataset['release'], format='ISO8601', errors='coerce')


filtered_df = new_df.rename(columns={'source': 'Dependencies', 'target': 'Artifact'})


gav_folder = os.path.join(data_folder, 'GAV')
os.makedirs(gav_folder, exist_ok=True)

chunk_size = 40000
num_chunks = (len(filtered_df) + chunk_size - 1) // chunk_size

for i in range(num_chunks):
    chunk = filtered_df[i*chunk_size:(i+1)*chunk_size]
    chunk_file = os.path.join(gav_folder, f'GAV{i+1}.csv')
    chunk.to_csv(chunk_file, index=False)

print("Files saved to Project/data/GAV")


plot_folder = os.path.join(os.getcwd(), 'plots')
os.makedirs(plot_folder, exist_ok=True)


filtered_df['dependency_release_year'] = filtered_df['dependency_release_date'].dt.year
yearly_counts = filtered_df.groupby('dependency_release_year').size()

new_dataset['release'] = new_dataset['release'].dt.year
yearly_counts_art = new_dataset.groupby('release').size()

plt.figure(figsize=(10, 6))
yearly_counts_art.plot(marker='o', linestyle='-')
plt.xlabel('GAV Release Year')
plt.ylabel('GAV Count')
plt.title('Count of GAV release across the years')
plt.grid(True)
plt.gca().yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
plt.ticklabel_format(style='plain', axis='y')
plot_file_path = os.path.join(plot_folder, 'GAV.png')
plt.savefig(plot_file_path)


table_file_path_dep = os.path.join(plot_folder, 'GAV.csv')
yearly_counts_art.to_csv(table_file_path_dep, header=['Count'], index_label='Artifact Release Year')

plt.close()

# Plot dependencies release years
plt.figure(figsize=(10, 6))
yearly_counts.plot(marker='o', linestyle='-')
plt.xlabel('Dependency Release Year')
plt.ylabel('Dependency Count')
plt.title('Count of Dependencies Released across the Years')
plt.grid(True)
plt.gca().yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
plt.ticklabel_format(style='plain', axis='y')
plot_file_path_art = os.path.join(plot_folder, 'dependencies_GAV.png')
plt.savefig(plot_file_path_art)
plt.close()

table_file_path_art = os.path.join(plot_folder, 'Dependency_counts.csv')
yearly_counts.to_csv(table_file_path_art, header=['Count'], index_label='Dependency Release Year')

print(f"Plot saved to {plot_file_path}")
