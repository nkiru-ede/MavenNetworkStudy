import os
import pandas as pd
import matplotlib.pyplot as plt

parent_folder_path = os.getcwd()


folder_path = os.path.join(parent_folder_path, "data", "GAV")
csv_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv') and file.startswith('GAV')]


concatenated_df = pd.DataFrame()


for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    concatenated_df = pd.concat([concatenated_df, df])



filtered_df = concatenated_df

df = pd.DataFrame(filtered_df, columns=["Dependencies", "Artifact", "dependency_release_date", "artifact_release_date"])

df["dependency_release_date"] = pd.to_datetime(df["dependency_release_date"])
df["artifact_release_date"] = pd.to_datetime(df["artifact_release_date"])

df["dependency_year"] = df["dependency_release_date"].dt.year

dependencies_by_year = df.groupby("dependency_year")["Dependencies"].count()

plt.figure(figsize=(10, 6))
plt.plot(dependencies_by_year.index, dependencies_by_year.values, marker='o', linestyle='-')

plt.xlabel('Year')
plt.ylabel('Count of Ggav')
plt.title('Growth of Ggav Over Years')
plt.grid(True)
plt.show()
