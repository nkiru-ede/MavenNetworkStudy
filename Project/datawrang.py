import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

data_folder = './data'
links_file = os.path.join(data_folder, 'links_all.csv')
release_file = os.path.join(data_folder, 'release_all.csv')


new_df = pd.read_csv(links_file, delimiter=',')
new_dataset = pd.read_csv(release_file, delimiter=',')

new_df.columns = new_df.columns.str.replace('"', '').str.strip()

# Clean column names and select required columns in new_dataset
print("Columns in new_dataset before cleaning:")
print(new_dataset.columns)


new_dataset.columns = new_dataset.columns.str.replace('"', '').str.strip()
new_dataset = new_dataset[['artifact', 'release']]  # Select only required columns


print("Columns in new_dataset after cleaning:")
print(new_dataset.columns)

new_df = new_df.merge(new_dataset, how='left', left_on='source', right_on='artifact')
new_df.rename(columns={'release': 'dependency_release_date'}, inplace=True)
new_df.drop(columns=['artifact'], inplace=True)

new_df = new_df.merge(new_dataset, how='left', left_on='target', right_on='artifact')
new_df.rename(columns={'release': 'artifact_release_date'}, inplace=True)
new_df.drop(columns=['artifact'], inplace=True)

new_df['dependency_release_date'] = new_df['dependency_release_date'].str.replace(r'\[GMT\]', '', regex=True)
new_df['artifact_release_date'] = new_df['artifact_release_date'].str.replace(r'\[GMT\]', '', regex=True)

new_df['dependency_release_date'] = pd.to_datetime(new_df['dependency_release_date'], format='ISO8601', errors='coerce')
new_df['artifact_release_date'] = pd.to_datetime(new_df['artifact_release_date'], format='ISO8601', errors='coerce')

filtered_df = new_df[new_df['dependency_release_date'] >= new_df['artifact_release_date']]
filtered_df = filtered_df.rename(columns={'source': 'Dependencies', 'target': 'Artifact'})

gav_folder = os.path.join(data_folder, 'GAV')
os.makedirs(gav_folder, exist_ok=True)

chunk_size = 40000
num_chunks = (len(filtered_df) + chunk_size - 1) // chunk_size

for i in range(num_chunks):
    chunk = filtered_df[i*chunk_size:(i+1)*chunk_size]
    chunk_file = os.path.join(gav_folder, f'GAV{i+1}.csv')
    chunk.to_csv(chunk_file, index=False)

print("Files saved to Project/data/GAV")

plot_folder = os.path.join(os.getcwd(), 'plots')
os.makedirs(plot_folder, exist_ok=True)

filtered_df['dependency_release_year'] = filtered_df['dependency_release_date'].dt.year
yearly_counts = filtered_df.groupby('dependency_release_year').size()

plt.figure(figsize=(10, 6))
yearly_counts.plot(marker='o', linestyle='-')

plt.xlabel('GAV Release Year')
plt.ylabel('GAV Count')
plt.title('Count of GAV release across the years')
plt.grid(True)

plt.gca().yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
plt.ticklabel_format(style='plain', axis='y')

plot_file_path = os.path.join(plot_folder, 'GAV.png')
plt.savefig(plot_file_path)
plt.close()

print(f"Plot saved to {plot_file_path}")
