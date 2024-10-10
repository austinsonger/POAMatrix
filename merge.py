import os
import re
import pandas as pd

# Constants
DIRECTORY = "./scans_directory"  # Replace with your directory path
OUTPUT_FILE = "merged_vulnerability_data.csv"
FILE_EXTENSION = ".csv"

def load_and_label_csv(file_path, scan_type):
    """Load a CSV file and add a column for scan type."""
    return pd.read_csv(file_path).assign(Scan_Type=scan_type)

def identify_scan_type(file_name):
    """Identify the scan type based on the file name using regex."""
    if re.search(r'AWS_CIS|STIG', file_name, re.IGNORECASE):
        return 'STIG Scan'
    else:
        return 'Vulnerability Scan'

def merge_csv_files(directory):
    """Merge CSV files found in a directory, labeling them by scan type."""
    dfs = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(FILE_EXTENSION):
                file_path = os.path.join(root, file)
                scan_type = identify_scan_type(file)
                dfs.append(load_and_label_csv(file_path, scan_type))
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