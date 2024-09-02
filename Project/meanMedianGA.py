# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 20:25:23 2024

@author: edenk
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_process_data(all_ga_file_path, top_100_file_path):
    df_all_ga = pd.read_csv(all_ga_file_path)
    df_top_100 = pd.read_csv(top_100_file_path)

    df_all_ga['component'] = df_all_ga['artifact'].apply(lambda x: ':'.join(x.split(':')[:2]))
    df_all_ga['release_year'] = df_all_ga['release'].str.split('-', n=2).str[0]
    df_all_ga['release_year'] = pd.to_numeric(df_all_ga['release_year'], errors='coerce')
    df_all_ga = df_all_ga.dropna(subset=['release_year'])

    # Process the 'Top 100 GA' dataset
    df_top_100['Artifact'] = df_top_100['Artifact'].astype(str)
    df_top_100['component'] = df_top_100['Artifact'].apply(lambda x: ':'.join(x.split(':')[:2]) if ':' in x else x)
    df_top_100['release_year'] = df_top_100['artifact_release_date'].str.split('-', n=2).str[0]
    df_top_100['release_year'] = pd.to_numeric(df_top_100['release_year'], errors='coerce')
    df_top_100 = df_top_100.dropna(subset=['release_year'])

    return df_all_ga, df_top_100


def compute_statistics(df_all_ga, df_top_100):
    component_counts_top_100 = df_top_100.groupby(['release_year', 'component']).size().reset_index(name='count')
    top_100_components = (component_counts_top_100
                          .groupby('release_year')
                          .apply(lambda x: x.nlargest(100, 'count'))
                          .reset_index(drop=True))
    top_100_unique_components = top_100_components['component'].unique()

    df_all_ga_top_100 = df_all_ga[df_all_ga['component'].isin(top_100_unique_components)]

    all_years = df_all_ga['release_year'].unique()
    all_components = df_all_ga['component'].unique()
    index = pd.MultiIndex.from_product([all_years, all_components], names=['release_year', 'component'])
    df_full = pd.DataFrame(index=index).reset_index()

    df_all_ga_counts = df_all_ga.groupby(['release_year', 'component']).size().reset_index(name='count')
    df_all_ga_full = pd.merge(df_full, df_all_ga_counts, on=['release_year', 'component'], how='left').fillna(0)

    medians_all = df_all_ga_full.groupby('release_year')['count'].median().reset_index(name='median_all')
    means_all = df_all_ga_full.groupby('release_year')['count'].mean().reset_index(name='mean_all')

    all_components_top_100 = df_all_ga_top_100['component'].unique()
    index_top_100 = pd.MultiIndex.from_product([all_years, all_components_top_100], names=['release_year', 'component'])
    df_full_top_100 = pd.DataFrame(index=index_top_100).reset_index()

    df_top_100_counts = df_all_ga_top_100.groupby(['release_year', 'component']).size().reset_index(name='count')
    df_all_ga_full_top_100 = pd.merge(df_full_top_100, df_top_100_counts, on=['release_year', 'component'], how='left').fillna(0)

    medians_top_100 = df_all_ga_full_top_100.groupby('release_year')['count'].median().reset_index(name='median_top_100')
    means_top_100 = df_all_ga_full_top_100.groupby('release_year')['count'].mean().reset_index(name='mean_top_100')

    return means_all, medians_all, means_top_100, medians_top_100

def print_statistics(means_all, medians_all, means_top_100, medians_top_100):
    print("Means and Medians for All GA and Top 100 GA by Year")
    print("\nAll GA:")
    print(means_all)
    print(medians_all)
    
    print("\nTop 100 GA:")
    print(means_top_100)
    print(medians_top_100)



if __name__ == "__main__":
    all_ga_file_path = 'C:/Users/edenk/.spyder-py3/data/release_all.csv'  # Replace with the actual path to your 'All GA' CSV file
    top_100_file_path = 'C:/Users/edenk/.spyder-py3/data/GA.csv'  # Replace with the actual path to your 'Top 100 GA' CSV file

    df_all_ga, df_top_100 = load_and_process_data(all_ga_file_path, top_100_file_path)
    
    means_all, medians_all, means_top_100, medians_top_100 = compute_statistics(df_all_ga, df_top_100)
    
    print_statistics(means_all, medians_all, means_top_100, medians_top_100)
