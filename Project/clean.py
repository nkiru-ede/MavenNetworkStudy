# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 11:50:10 2024

@author: Nkiru.Ede
"""

import pandas as pd

# Load the CSV files
source_target_df = pd.read_csv("C:\\Users\\Nkiru.Ede\\Downloads\\links_all_new.csv") 
artifact_release_df = pd.read_csv("C:\\Users\\Nkiru.Ede\\Downloads\\release_all_new.csv")  

artifact_release_df.rename(columns={'Artifact': 'source'}, inplace=True)

merged_source = pd.merge(source_target_df, artifact_release_df, on='source', how='left')

# Rename the 'release' column for source
merged_source.rename(columns={'release': 'source_release'}, inplace=True)

# Now merge again to get the target_release
artifact_release_df.rename(columns={'source': 'target'}, inplace=True)  # Rename back for merging
merged_final = pd.merge(merged_source, artifact_release_df[['target', 'release']], on='target', how='left')

# Rename the 'release' column for target
merged_final.rename(columns={'release': 'target_release'}, inplace=True)

# Count the number of populated fields in source_release and target_release
source_release_count = merged_final['source_release'].notnull().sum()
target_release_count = merged_final['target_release'].notnull().sum()

print(f'Number of populated fields in source_release: {source_release_count}')
print(f'Number of populated fields in target_release: {target_release_count}')
