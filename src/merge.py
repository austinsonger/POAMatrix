import os
import re
import pandas as pd

# Constants
DIRECTORY = "./fake-testdata"  
OUTPUT_FILE = "./output/merged_vulnerability_data.csv"
FILE_EXTENSION = ".csv"

def load_and_label_csv(file_path, scan_type):
    """Load a CSV file and add a column for scan type."""
    try:
        return pd.read_csv(file_path).assign(Scan_Type=scan_type)
    except pd.errors.ParserError:
        print(f"Error parsing {file_path}. Check for format issues.")
        return pd.DataFrame()

def identify_scan_type(file_name):
    """Identify the scan type based on the file name using regex."""
    if re.search(r'AWS_CIS|STIG', file_name, re.IGNORECASE):
        return 'STIG Scan'
    else:
        return 'Vulnerability Scan'

def split_multi_value_column(df, column_name):
    """Split multi-value entries in the specified column into separate rows."""
    # Expand rows where the column contains multiple values
    df_expanded = df.dropna(subset=[column_name]).copy()
    df_expanded[column_name] = df_expanded[column_name].str.split('\n')
    df_expanded = df_expanded.explode(column_name).reset_index(drop=True)
    
    # Combine expanded rows back with non-expanded rows
    df_non_expanded = df[df[column_name].isna()].copy()
    df_final = pd.concat([df_expanded, df_non_expanded], ignore_index=True)
    
    return df_final

def merge_csv_files(directory):
    """Merge CSV files found in a directory, labeling them by scan type."""
    dfs = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(FILE_EXTENSION):
                file_path = os.path.join(root, file)
                scan_type = identify_scan_type(file)
                df = load_and_label_csv(file_path, scan_type)
                if not df.empty:
                    # If there is a "Weakness Description" column, apply the splitting
                    if "Weakness Description" in df.columns:
                        df = split_multi_value_column(df, "Weakness Description")
                    dfs.append(df)
    merged_df = pd.concat(dfs, join="outer", ignore_index=True)
    # Move 'Scan_Type' column to the front
    columns = ['Scan_Type'] + [col for col in merged_df.columns if col != 'Scan_Type']
    return merged_df[columns]

def save_to_csv(df, output_file):
    """Save the DataFrame to a CSV file."""
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    merged_df = merge_csv_files(DIRECTORY)
    save_to_csv(merged_df, OUTPUT_FILE)
    print(f"Merged CSV saved to {OUTPUT_FILE}")