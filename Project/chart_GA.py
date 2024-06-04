# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 16:10:44 2024

@author: edenk
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

parent_folder_path = os.getcwd()

folder_path = os.path.join(parent_folder_path, "data", "GA")
csv_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv') and file.startswith('GA')]

concatenated_df = pd.DataFrame()

for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    concatenated_df = pd.concat([concatenated_df, df])

filtered_df = concatenated_df

df = pd.DataFrame(filtered_df)

df["dependency_release_date"] = pd.to_datetime(df["Source Release Year"])
#df["artifact_release_date"] = pd.to_datetime(df["artifact_release_date"])

#df["dependency_year"] = df["dependency_release_date"].dt.year

dependencies_by_year = df.groupby("dependency_release_date")["Source_Group_Id"].count()

plt.figure(figsize=(10, 6))
plt.plot(dependencies_by_year.index, dependencies_by_year.values, marker='o', linestyle='-')

plt.xlabel('Year')
plt.ylabel('Count of GA')
plt.title('Growth of GA Over Years')
plt.grid(True)
plt.show()
