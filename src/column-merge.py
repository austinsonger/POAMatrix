import os
import pandas as pd

# Constants
INPUT_FILE = "./fake-testdata/Inspector.csv"  # Path to your target file
OUTPUT_FILE = "./output/merged_check_id_title.csv"

def load_csv(file_path):
    """Load the CSV file."""
    try:
        print(f"Loading file: {file_path}")
        df = pd.read_csv(file_path, encoding='utf-8')  # Ensure UTF-8 encoding
        print(f"Columns found: {list(df.columns)}")
        return df
    except pd.errors.ParserError as e:
        print(f"Error parsing {file_path}: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Unexpected error loading {file_path}: {e}")
        return pd.DataFrame()

def merge_check_id_and_title(df):
    """Merge 'check_id' and 'title' columns and remove the originals."""
    if 'check_id' in df.columns and 'title' in df.columns:
        print("Merging 'check_id' and 'title' columns...")
        # Create the merged column, handling any NaN values gracefully
        df['merged'] = df['check_id'].fillna('N/A').astype(str) + ' - ' + df['title'].fillna('N/A').astype(str)
        print("Merge successful. Sample output:")
        print(df[['merged']].head())  # Show sample merged data
        
        # Drop the old columns
        df = df.drop(['check_id', 'title'], axis=1)
    else:
        missing_cols = [col for col in ['check_id', 'title'] if col not in df.columns]
        print(f"Missing columns: {missing_cols}.")
    return df

def save_to_csv(df, output_file):
    """Save the DataFrame to a CSV file with proper quoting."""
    try:
        # Ensure proper quoting for multiline fields
        df.to_csv(output_file, index=False, quoting=2)  # quoting=2 means QUOTE_NONNUMERIC
        print(f"Merged CSV saved to {output_file}")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    # Check if the input file exists
    if os.path.exists(INPUT_FILE):
        df = load_csv(INPUT_FILE)
        if not df.empty:
            merged_df = merge_check_id_and_title(df)
            save_to_csv(merged_df, OUTPUT_FILE)
        else:
            print(f"No data found in {INPUT_FILE}.")
    else:
        print(f"File {INPUT_FILE} not found.")