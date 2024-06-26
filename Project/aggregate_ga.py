import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

def process_merged_GA(path):
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

        # Check if the expected columns are present
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

    grouped_df = merged_GA_df.groupby('Target Release Year')['Target_Artifact_Id'].count()

    plt.figure(figsize=(10, 6))
    grouped_df.plot(marker='o', linestyle='-')

    plt.xlabel('GA Release Year')
    plt.ylabel('GA Count')
    plt.title('Count of GA release across the years')
    plt.grid(True)
    
    plt.gca().yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    plt.ticklabel_format(style='plain', axis='y')
    
    plt.gca().xaxis.set_major_formatter(ScalarFormatter())
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))


    # Save the plot to a file
    plot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plots")
    os.makedirs(plot_dir, exist_ok=True)
    plot_file_path = os.path.join(plot_dir, "GA_Growth.png")
    plt.savefig(plot_file_path)
    #plt.show()
    
    # Save the yearly counts as CSV files
    table_file_path_dep = os.path.join(plot_dir, 'GA_Growth.csv')
    grouped_df.to_csv(table_file_path_dep, header=['Count'], index_label='GA Release Year')
    
    
    grouped_dfs = merged_GA_df.groupby('Source Release Year')['Source_Artifact_Id'].count()

    plt.figure(figsize=(10, 6))
    grouped_dfs.plot(marker='o', linestyle='-')
    
    
    plt.xlabel('Dependency Release Year(GA)')
    plt.ylabel('Dependency Count(GA)')
    plt.title('Count of dependencies release across the years (GA)')
    plt.grid(True)
    
    plt.gca().yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    plt.ticklabel_format(style='plain', axis='y')
    
    plt.gca().xaxis.set_major_formatter(ScalarFormatter())
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    
    # Save the plot to a file
    plot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plots")
    os.makedirs(plot_dir, exist_ok=True)
    plot_file_path = os.path.join(plot_dir, "Dependencies_Growth(GA).png")
    plt.savefig(plot_file_path)
    #plt.show()
    
    
    # Save the yearly counts as CSV files
    table_file_path_dep = os.path.join(plot_dir, 'Dependencies_Growth(GA).csv')
    grouped_dfs.to_csv(table_file_path_dep, header=['Count'], index_label='Dependency(GA) Release Year')

    merged_GA_df = merged_GA_df.drop(columns=['Source Release Date', 'Target Release Date'], errors='ignore')

    current_dir = os.path.dirname(os.path.abspath(__file__))
    merged_GA_df.to_csv(os.path.join(current_dir, "data", "GA.csv"), index=False)

    return merged_GA_df

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_folder_path = os.path.join(current_dir, "data", "GAV")
    merged_GA_df = process_merged_GA(csv_folder_path)
    print("GA DataFrame:")
    print(merged_GA_df)
    print(len(merged_GA_df))
    print("GA saved to Project/data/GA.csv")
    print("GA Growth chart saved to Project/plot")
