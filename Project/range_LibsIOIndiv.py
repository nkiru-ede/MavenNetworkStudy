import pandas as pd
import re

def percentage_maven_targets_with_ranges(df):
    # regex patterns for ranges
    range_patterns = [
        r"^\s*>[=v\s]*[^<]*<.*$",
        r"^[=v\s]*[xX\*\d]+(\.[xX\*\d]+){0,2}(-[\.\w]+)?\s+-\s+[=v\s]*[xX\*\d]+(\.[xX\*\d]+){0,2}(-.*)?$",
        r"^\s*<[^>]+>.*$"
    ]
    
    # Filter platform
    platform_df = df[df['Platform'] == 'npm'].copy()
    
    # does target matches any range pattern?
    def has_range(target):
        return any(re.search(pattern, str(target)) for pattern in range_patterns)
    
    # Count records with ranges
    platform_df['HasRange'] = platform_df['target'].apply(has_range)
    
    # Calculate percentage
    total_maven = len(platform_df)
    matching_maven = platform_df['HasRange'].sum()
    percentage = (matching_maven / total_maven) * 100 if total_maven > 0 else 0
    
    return percentage

df = pd.read_csv("C:\\Users\\edenk\\.spyder-py3\\data\\libsIO\\links_all_Libs.csv")

percentage = percentage_maven_targets_with_ranges(df)
print(f"Percentage of Maven records with target in range format: {percentage:.4f}%")
