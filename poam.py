import pandas as pd

# Load files
merged_vulnerability_data_path = 'merged_vulnerability_data.csv'  # Path to CSV file
poam_excel_path = 'poam/poam.xlsx'  # Path to poam Excel file

# Load the "merged_vulnerability_data" as CSV and the poam Excel file, skipping the first two rows
merged_df = pd.read_csv(merged_vulnerability_data_path, skiprows=2)
poam_df = pd.read_excel(poam_excel_path, skiprows=2, engine='openpyxl')

# Debug: Print column names to inspect and debug
print("Merged Vulnerability Data Columns:", merged_df.columns)

# Inspect the first few rows to identify the correct columns
print(merged_df.head())

# Mapping based on YAML and the Tenable columns
mapping = {
    "Plugin": "Weakness Source Identifier",  # Adjusted to match the actual column name for Plugin ID
    "Name": "Weakness Name",
    "Risk": "Original Risk Rating",
    "Host": "Asset Identifier",
    "First Found": "Discovery Date",
    "Last Found": "Last Changed or Closed",
    "Description": "Weakness Description",
    "Solution": "Remediation Plan",
    "Patch Available": "Remediation Plan"
}

# Check for new vulnerabilities
for _, row in merged_df.iterrows():
    try:
        plugin_id = row['Plugin']  # Use the updated 'Plugin' column name
        host = row['Host']  # Ensure 'Host' is the correct column
        
        # Check if this combination of Plugin ID and Host exists in the poam
        is_new = poam_df[
            (poam_df['Weakness Source Identifier'] == plugin_id) &
            (poam_df['Asset Identifier'] == host)
        ].empty
        
        if is_new:
            # Find the first empty row in the poam to add the new vulnerability
            empty_row_index = poam_df[poam_df.isnull().all(axis=1)].index[0]
            
            # Populate the new row using the mappings
            for tenable_col, poam_col in mapping.items():
                poam_df.loc[empty_row_index, poam_col] = row[tenable_col]
    
    except KeyError as e:
        print(f"Column missing: {e}")
    except IndexError:
        print("No empty rows available in the poam for new vulnerabilities.")
        break

# Save the updated poam back to an Excel file
updated_poam_excel_path = 'poam/updated_poam.xlsx'  # Path to save updated poam
poam_df.to_excel(updated_poam_excel_path, index=False, engine='openpyxl')

print(f"Updated poam saved to {updated_poam_excel_path}")