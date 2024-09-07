# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 00:08:29 2024

@author: edenk
"""

import pandas as pd
import numpy as np

def calculate_gini_from_csv(file_path):
    def gini_coefficient(x):
        """Compute Gini coefficient for an array x."""
        # Ensure all dependency counts are non-negative
        x = np.array(x, dtype=float)

        # Sort the array
        x.sort()

        # Compute the cumulative sum of the array
        cumulative_sum = np.cumsum(x)

        # The population index
        n = len(x)

        # Sum of all elements
        total_sum = cumulative_sum[-1]

        # If total sum is zero, return Gini as 0 (all equal)
        if total_sum == 0:
            return 0.0

        # Compute Lorenz curve values
        lorenz_curve = cumulative_sum / total_sum

        # Calculate Gini coefficient
        gini = 1 - (2 / n) * np.sum(lorenz_curve) + (1 / n)

        return gini

    # Load the CSV file
    df = pd.read_csv(file_path, encoding='ISO-8859-1')

    # Convert 'dependency_release_date' to datetime format and extract the year
    df['dependency_release_year'] = pd.to_datetime(df['dependency_release_date']).dt.year

    # Group by 'Artifact' and 'dependency_release_year', count the dependencies
    artifact_dependency_counts = df.groupby(['Artifact', 'dependency_release_year'])['Dependencies'].count().reset_index()

    # Rename the 'Dependencies' column to 'dependency_count'
    artifact_dependency_counts.rename(columns={'Dependencies': 'dependency_count'}, inplace=True)

    # calculate Gini coefficient per year
    def compute_gini_per_year(df):
        # Group by the release year
        gini_per_year = {}
        for year, group in df.groupby('dependency_release_year'):
            gini = gini_coefficient(group['dependency_count'])
            gini_per_year[year] = gini
        return gini_per_year

    # Compute Gini coefficients for each year
    gini_per_year = compute_gini_per_year(artifact_dependency_counts)

    # Return the Gini coefficients per year
    return gini_per_year

#usage:
#file_path = './data/merged_gav.csv'

#gini_per_year = calculate_gini_from_csv(file_path)

# Print the Gini coefficients per year
#for year, gini in gini_per_year.items():
 #   print(f"Gini coefficient for year {year}: {gini:.4f}")
