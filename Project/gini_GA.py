# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 10:16:24 2024

@author: edenk
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analyze_gini_and_plot(file_path):
    # Load the data
    df = pd.read_csv(file_path)

    # Preprocessing: Remove versions from Dependencies and Artifact columns
    df['Dependencies'] = df['Dependencies'].str.split(':').str[0]
    df['Artifact'] = df['Artifact'].str.split(':').str[0]

    # Grouping the data by 'Source Release Year' and 'Dependencies'
    grouped = df.groupby(['Source Release Year', 'Dependencies']).size().reset_index(name='Count')

    # Function to calculate the Gini coefficient
    def gini_coefficient(x):
        x_sorted = np.sort(x)  # Sort values
        n = len(x)
        index = np.arange(1, n + 1)
        gini = (2 * np.sum(index * x_sorted) - (n + 1) * np.sum(x_sorted)) / (n * np.sum(x_sorted))
        return gini

    # Calculate the Gini coefficient for each year
    gini_coeffs = grouped.groupby('Source Release Year')['Count'].apply(gini_coefficient)

    # Print the Gini coefficients for each year
    print(gini_coeffs)

    # Plotting the Lorenz Curves
    plt.figure(figsize=(10, 6))

    for year, group in grouped.groupby('Source Release Year'):
        sorted_group = group['Count'].sort_values()
        cum_pop = np.cumsum(sorted_group) / sorted_group.sum()
        cum_wealth = np.arange(1, len(sorted_group) + 1) / len(sorted_group)

        plt.plot(cum_wealth, cum_pop, label=f'Year {year}')

    # Plot the line of equality
    plt.plot([0,1], [0,1], 'k--')

    plt.xlabel('Cumulative Proportion of Vertecies')
    plt.ylabel('Cumulative Proportion of Edges')
    plt.title('Lorenz Curve by Year')
    plt.legend(title="Year")
    plt.show()

    # Optional: Plotting Gini coefficient over time
    plt.figure(figsize=(10, 6))
    gini_coeffs.plot(marker='o')
    plt.xlabel('Year')
    plt.ylabel('Gini Coefficient')
    plt.title('Gini Coefficient Over Time')
    plt.show()

analyze_gini_and_plot('./data/GA.csv')
