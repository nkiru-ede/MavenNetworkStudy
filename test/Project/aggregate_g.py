import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter


def process_merged_G(path):
    if os.path.isdir(path):
        csv_files = [os.path.join(path, file_name) for file_name in os.listdir(path) if file_name.endswith('.csv') and file_name.startswith('GAV')]
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
        
        expected_columns = ['Artifact', 'Dependencies', 'artifact_release_date', 'dependency_release_date']
        if not all(col in df.columns for col in expected_columns):
            raise ValueError("CSV file does not contain the required columns.")

        new_df = df[['Artifact', 'Dependencies', 'artifact_release_date', 'dependency_release_date']].copy()
        new_df[['Target_Group_Id', 'Target_Artifact_Id', 'Target_Version']] = df['Artifact'].str.split(':', expand=True)
        new_df[['Source_Group_Id', 'Source_Artifact_Id', 'Source_Version']] = df['Dependencies'].str.split(':', expand=True)

        df.drop(columns=['Artifact', 'Dependencies'], inplace=True)
        df = df.rename(columns={'artifact_release_date': 'Target Release Date', 'dependency_release_date': 'Source Release Date'})

        df['Target Release Year'] = df['Target Release Date'].str[:4]
        df['Source Release Year'] = df['Source Release Date'].str[:4]
        
        df = df[df['Target Release Year'].str.isnumeric()]
        df = df[df['Source Release Year'].str.isnumeric()]

        df['Target Release Year'] = df['Target Release Year'].astype(int)
        df['Source Release Year'] = df['Source Release Year'].astype(int)

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
    merged_G_df = merged_G_df.drop(columns=['Source Release Date', 'Target Release Date'], errors='ignore')

    current_dir = os.path.dirname(os.path.abspath(__file__))
    merged_G_df.to_csv(os.path.join(current_dir, "data","G.csv"), index=False)

    grouped_df = merged_G_df.groupby('Target Release Year')['Target_Group_Id'].count()

    plt.figure(figsize=(10, 6))
    grouped_df.plot(marker='o', linestyle='-')

    plt.xlabel('G Release Year')
    plt.ylabel('G Count')
    plt.title('Count of G release across the years')
    plt.grid(True)
    #plt.show()
    
    plt.gca().yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    plt.ticklabel_format(style='plain', axis='y')
    
    plt.gca().xaxis.set_major_formatter(ScalarFormatter())
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    
    # Save the plot to a file
    plot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plots")
    os.makedirs(plot_dir, exist_ok=True)
    plot_file_path = os.path.join(plot_dir, "G_Growth.png")
    plt.savefig(plot_file_path)
    plt.show()
    
    # Save the yearly counts as CSV files
    table_file_path_dep = os.path.join(plot_dir, 'G_Growth.csv')
    grouped_df.to_csv(table_file_path_dep, header=['Count'], index_label='G Release Year')
    
    
    
    grouped_dfs = merged_G_df.groupby('Source Release Year')['Source_Group_Id'].count()

    plt.figure(figsize=(10, 6))
    grouped_dfs.plot(marker='o', linestyle='-')
    
    
    plt.xlabel('Dependency Release Year(G)')
    plt.ylabel('Dependency Count(G)')
    plt.title('Count of dependencies release across the years (G)')
    plt.grid(True)
    
    plt.gca().yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    plt.ticklabel_format(style='plain', axis='y')
    
    plt.gca().xaxis.set_major_formatter(ScalarFormatter())
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    
    # Save the plot to a file
    plot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plots")
    os.makedirs(plot_dir, exist_ok=True)
    plot_file_path = os.path.join(plot_dir, "Dependencies_Growth(G).png")
    plt.savefig(plot_file_path)
    #plt.show()
    
    
    # Save the yearly counts as CSV files
    table_file_path_dep = os.path.join(plot_dir, 'Dependencies_Growth(G).csv')
    grouped_dfs.to_csv(table_file_path_dep, header=['Count'], index_label='Dependency(G) Release Year')
    
    
    
    






    return merged_G_df

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_folder_path = os.path.join(current_dir, "data", "GAV")
    merged_G_df = process_merged_G(csv_folder_path)
    print("G DataFrame:")
    print(merged_G_df)
    print(len(merged_G_df))
    
  
    print("G saved to Project/data/G.csv")
    print("G Growth chart saved to Project/plot")
