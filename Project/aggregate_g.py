import pandas as pd
import os

def process_merged_G(path):
    if os.path.isdir(path):
        csv_files = [os.path.join(path, file_name) for file_name in os.listdir(path) if file_name.endswith('.csv')]
    elif os.path.isfile(path):
        csv_files = [path]
    else:
        raise FileNotFoundError(f"No CSV files found at '{path}'.")

    dfs = []

    for csv_file_path in csv_files:
        valid_rows = []
        with open(csv_file_path, "r") as file:
            for line in file:
                try:
                    row = line.strip().split(",")
                    valid_rows.append(row)
                except Exception as e:
                    print(f"Skipping row due to error: {e}")

        df = pd.DataFrame(valid_rows)

        df.columns = df.iloc[0]
        df = df[1:]
        df = df.rename_axis(None, axis=1)

        new_df = df[['Artifact', 'Dependencies', 'Upstream Release Date', 'Dependency Release Date']].copy()

        new_df[['Source_Group_Id', 'Source_Artifact_Id', 'Source_Version']] = df['Artifact'].str.split(':', expand=True)
        new_df[['Target_Group_Id', 'Target_Artifact_Id', 'Target_Version']] = df['Dependencies'].str.split(':', expand=True)

        df.drop(columns=['Artifact', 'Dependencies'], inplace=True)

        df = df.rename(columns={'Upstream Release Date': 'Source Release Date', 'Dependency Release Date': 'Target Release Date'})

        df['Source Release Year'] = df['Source Release Date'].str[:4]
        df['Target Release Year'] = df['Target Release Date'].str[:4]

        df = pd.concat([df, new_df], axis=1)

        desired_columns_order = ['Source_Group_Id', 'Source_Artifact_Id', 'Source Release Date', 'Source Release Year',
                                 'Target_Group_Id', 'Target_Artifact_Id', 'Target Release Date', 'Target Release Year']

        df = df[desired_columns_order]

        df_G = df.drop(columns=['Source_Artifact_Id', 'Target_Artifact_Id', 'Source_Version', 'Target_Version'], errors='ignore')
        filtered_dfs_G = []
        for year, group in df_G.groupby('Target Release Year'):
            filtered_group_G = group.drop_duplicates(subset=['Target_Group_Id'])
            filtered_dfs_G.append(filtered_group_G)
        filtered_df_G = pd.concat(filtered_dfs_G)

        grouped_G_df = filtered_df_G.groupby(['Target_Group_Id'])
        agg_G_df = grouped_G_df.agg(
            Target_First_Release_Date=('Target Release Date', 'min'),
            Target_Last_Release_Date=('Target Release Date', 'max'),
            Target_Version_Count=('Target_Group_Id', 'size'),
            Source_First_Release_Date=('Source Release Date', 'min'),
            Source_Last_Release_Date=('Source Release Date', 'max'),
            Source_Version_Count=('Source_Group_Id', 'size')
        ).reset_index()

        merged_G_df = pd.merge(filtered_df_G, agg_G_df, on=['Target_Group_Id'])

        dfs.append(merged_G_df)

    merged_G_df = pd.concat(dfs)
    return merged_G_df

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_folder_path = os.path.join(current_dir, "data", "GAV")
    merged_G_df = process_merged_G(csv_folder_path)
    print("G DataFrame:")
    print(merged_G_df)
    print(len(merged_G_df))
