import os
import pandas as pd
import matplotlib.pyplot as plt

parent_folder_path = os.getcwd()

folder_path = os.path.join(parent_folder_path, "data", "G")

csv_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv') and file.startswith('G')]

concatenated_df = pd.DataFrame()

for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    concatenated_df = pd.concat([concatenated_df, df], ignore_index=True)

print("Column names:", concatenated_df.columns)

if 'Source Release Year' in concatenated_df.columns:
    # Inspect the data to find non-numeric values
    print("Unique values in 'Source Release Year':", concatenated_df['Source Release Year'].unique())

    valid_years = concatenated_df['Source Release Year'].str.match(r'^\d{4}$')
    filtered_df = concatenated_df[valid_years]

    filtered_df["dependency_release_date"] = pd.to_datetime(filtered_df["Source Release Year"], format='%Y')

    dependencies_by_year = filtered_df.groupby("dependency_release_date")["Source_Group_Id"].count()

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(dependencies_by_year.index, dependencies_by_year.values, marker='o', linestyle='-')
    

    plt.xlabel('Year')
    plt.ylabel('Count of G')
    plt.title('Growth of G Over Years')
    plt.grid(True)
    plt.show()
else:
    print("The column 'Source Release Year' does not exist in the DataFrame.")
