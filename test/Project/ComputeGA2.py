# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 10:24:05 2024

@author: edenk
"""

import pandas as pd

def compute_counts(df):
    df['dependency_release_date'] = pd.to_datetime(df['dependency_release_date'])
    df['artifact_release_date'] = pd.to_datetime(df['artifact_release_date'])

    earliest_dependency_dates = df.groupby('Dependencies')['dependency_release_date'].min().reset_index()
    earliest_artifact_dates = df.groupby('Artifact')['artifact_release_date'].min().reset_index()

    earliest_dependency_dates['Year'] = earliest_dependency_dates['dependency_release_date'].dt.year
    earliest_artifact_dates['Year'] = earliest_artifact_dates['artifact_release_date'].dt.year

    dependency_counts = earliest_dependency_dates.groupby('Year').size().reset_index(name='Count of Dependencies')
    artifact_counts = earliest_artifact_dates.groupby('Year').size().reset_index(name='Count of Artifacts')

    return dependency_counts, artifact_counts
