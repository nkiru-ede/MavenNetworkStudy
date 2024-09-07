# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 15:55:52 2024

@author: edenk
"""

import pandas as pd

def process_artifacts(file_path):
    df = pd.read_csv(file_path, encoding='ISO-8859-1') 

    # Convert 'artifact_release_date' to datetime format and extract the year
    df['dependency_release_year'] = pd.to_datetime(df['dependency_release_date']).dt.year

    # Aggregate the 'Artifact' by removing the version part (assuming version is separated by a colon)
    df['aggregated_artifact'] = df['Artifact'].str.split(':').str[:2].str.join(':')

    # Group by 'aggregated_artifact' and 'dependency_release_year', count the dependencies
    artifact_dependency_counts = df.groupby(['aggregated_artifact', 'dependency_release_year'])['Dependencies'].count().reset_index()

    # Rename the 'Dependencies' column to 'dependency_count'
    artifact_dependency_counts.rename(columns={'Dependencies': 'dependency_count'}, inplace=True)

    # Sort by artifact release year and dependency count
    artifact_dependency_counts = artifact_dependency_counts.sort_values(by=['dependency_release_year', 'dependency_count'], ascending=[True, False])

    # Return the processed DataFrame
    return artifact_dependency_counts

def get_top_10_per_year(df):
    top_10_per_year = {}
    for year, group in df.groupby('dependency_release_year'):
        top_10_per_year[year] = group.head(10)
    return top_10_per_year
