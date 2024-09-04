# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 20:25:23 2024

@author: edenk
"""
"corrected - 04/09"
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

    first_release_year = df_all_ga.groupby('component')['release_year'].min().reset_index(name='first_release_year')

    df_all_ga_counts = df_all_ga.groupby(['release_year', 'component']).size().reset_index(name='count')
    df_all_ga_full = pd.merge(df_full, df_all_ga_counts, on=['release_year', 'component'], how='left').fillna(0)

    df_all_ga_full_filtered = pd.merge(df_all_ga_full, first_release_year, on='component')
    df_all_ga_full_filtered = df_all_ga_full_filtered[df_all_ga_full_filtered['first_release_year'] <= df_all_ga_full_filtered['release_year']]

    # Merge df_all_ga_full_filtered with top_100_unique_components
    df_all_ga_top_100_filtered = df_all_ga_full_filtered[df_all_ga_full_filtered['component'].isin(top_100_unique_components)]

    total_counts_all = df_all_ga_full_filtered.groupby('release_year')['count'].sum().reset_index(name='total_count_all')
    unique_components_all = df_all_ga_full_filtered.groupby('release_year')['component'].count().reset_index(name='unique_components_all')

    means_all = pd.merge(total_counts_all, unique_components_all, on='release_year')
    means_all['mean_all'] = means_all['total_count_all'] / means_all['unique_components_all']
    means_all = means_all[['release_year', 'mean_all']]

    medians_all = df_all_ga_full_filtered.groupby('release_year')['count'].median().reset_index(name='median_all')

    # Compute statistics for df_all_ga_top_100_filtered
    total_counts_top_100 = df_all_ga_top_100_filtered.groupby('release_year')['count'].sum().reset_index(name='total_count_top_100')
    unique_components_top_100 = df_all_ga_top_100_filtered.groupby('release_year')['component'].count().reset_index(name='unique_components_top_100')

    means_top_100 = pd.merge(total_counts_top_100, unique_components_top_100, on='release_year')
    means_top_100['mean_top_100'] = means_top_100['total_count_top_100'] / means_top_100['unique_components_top_100']
    means_top_100 = means_top_100[['release_year', 'mean_top_100']]

    medians_top_100 = df_all_ga_top_100_filtered.groupby('release_year')['count'].median().reset_index(name='median_top_100')

    print("\nTotal Counts for 2010:")
    print(total_counts_all[total_counts_all['release_year'] == 2009])

    print("\nUnique Components for 2010:")
    print(unique_components_all[unique_components_all['release_year'] == 2009])

    return means_all, medians_all, means_top_100, medians_top_100

def print_statistics(means_all, medians_all, means_top_100, medians_top_100):
    print("Means and Medians for All GA and Top 100 GA by Year")
    print("\nAll GA:")
    print(means_all)
    print(medians_all)
    
    print("\nTop 100 GA:")
    print(means_top_100)
    print(medians_top_100)


def plot_statistics(means_all, medians_all, means_top_100, medians_top_100):
    plt.figure(figsize=(12, 6))
    
    # Plot means
    sns.lineplot(x='release_year', y='mean_all', data=means_all, label='Mean All GA', marker='o')
    sns.lineplot(x='release_year', y='mean_top_100', data=means_top_100, label='Mean Top 100 GA', marker='o')
    
    # Plot medians
    sns.lineplot(x='release_year', y='median_all', data=medians_all, label='Median All GA', marker='x')
    sns.lineplot(x='release_year', y='median_top_100', data=medians_top_100, label='Median Top 100 GA', marker='x')

    plt.title('Means and Medians of All GA and Top 100 GA over Time')
    plt.xlabel('Release Year')
    plt.ylabel('Count')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # Show the plot
    plt.show()
if __name__ == "__main__":
    all_ga_file_path = 'C:/Users/edenk/.spyder-py3/data/release_all.csv' 
    top_100_file_path = 'C:/Users/edenk/.spyder-py3/data/GA.csv' 
    
    #all_ga_file_path = 'C:/Users/edenk/.spyder-py3/data/release_allTest.csv' 
    #top_100_file_path = 'C:/Users/edenk/.spyder-py3/data/GA_test.csv' 
    

    df_all_ga, df_top_100 = load_and_process_data(all_ga_file_path, top_100_file_path)
    
    means_all, medians_all, means_top_100, medians_top_100 = compute_statistics(df_all_ga, df_top_100)
    
    print_statistics(means_all, medians_all, means_top_100, medians_top_100)
    
    plot_statistics(means_all, medians_all, means_top_100, medians_top_100)
