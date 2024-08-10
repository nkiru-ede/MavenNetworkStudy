# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 20:10:24 2024

@author: edenk
"""

import pandas as pd

def compute_counts_GA3(df):
    df['dependency_release_date'] = pd.to_datetime(df['dependency_release_date'])
    df['artifact_release_date'] = pd.to_datetime(df['artifact_release_date'])

    latest_dependency_dates = df.groupby('Dependencies')['dependency_release_date'].max().reset_index()
    latest_artifact_dates = df.groupby('Artifact')['artifact_release_date'].max().reset_index()

    latest_dependency_dates['Year'] = latest_dependency_dates['dependency_release_date'].dt.year
    latest_artifact_dates['Year'] = latest_artifact_dates['artifact_release_date'].dt.year

    dependency_counts = latest_dependency_dates.groupby('Year').size().reset_index(name='Count of Dependencies')
    artifact_counts = latest_artifact_dates.groupby('Year').size().reset_index(name='Count of Artifacts')

    return dependency_counts, artifact_counts