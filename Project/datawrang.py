import pandas as pd
import os


data_folder = './data'
links_file = os.path.join(data_folder, 'links_all.csv')
release_file = os.path.join(data_folder, 'release_all.csv')


new_df = pd.read_csv(links_file, delimiter=',')
new_dataset = pd.read_csv(release_file, delimiter=',')


new_dataset.columns = new_dataset.columns.str.replace('"', '').str.strip()


new_df = new_df.merge(new_dataset[['artifact', 'release']], how='left', left_on='source', right_on='artifact')
new_df.rename(columns={'release': 'dependency_release_date'}, inplace=True)
new_df.drop(columns=['artifact'], inplace=True)

new_df = new_df.merge(new_dataset[['artifact', 'release']], how='left', left_on='target', right_on='artifact')
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
