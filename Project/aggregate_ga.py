import pandas as pd
import os

def process_merged_GA(path):
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

        desired_columns_order = ['Source_Group_Id', 'Source_Artifact_Id', 'Source_Version', 'Source Release Date', 'Source Release Year',
                                 'Target_Group_Id', 'Target_Artifact_Id', 'Target_Version', 'Target Release Date', 'Target Release Year']

        df = df[desired_columns_order]

        df_GA = df.drop(columns=['Source_Version', 'Target_Version'], errors='ignore')
        filtered_dfs_GA = []
        for year, group in df_GA.groupby('Target Release Year'):
            filtered_group_GA = group.drop_duplicates(subset=['Target_Group_Id', 'Target_Artifact_Id'])
            filtered_dfs_GA.append(filtered_group_GA)
        filtered_df_GA = pd.concat(filtered_dfs_GA)

        grouped_GA_df = filtered_df_GA.groupby(['Target_Group_Id', 'Target_Artifact_Id'])
        agg_GA_df = grouped_GA_df.agg(
            Target_First_Release_Date=('Target Release Date', 'min'),
            Target_Last_Release_Date=('Target Release Date', 'max'),
            Target_Version_Count=('Target_Artifact_Id', 'size'),
            Source_First_Release_Date=('Source Release Date', 'min'),
            Source_Last_Release_Date=('Source Release Date', 'max'),
            Source_Version_Count=('Source_Artifact_Id', 'size')
        ).reset_index()

        merged_GA_df = pd.merge(filtered_df_GA, agg_GA_df, on=['Target_Group_Id', 'Target_Artifact_Id'])

        dfs.append(merged_GA_df)

    merged_GA_df = pd.concat(dfs)

    return merged_GA_df

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_folder_path = os.path.join(current_dir, "data", "GAV")
    merged_GA_df = process_merged_GA(csv_folder_path)
    print("GA DataFrame:")
    print(merged_GA_df)
    print(len(merged_GA_df))
