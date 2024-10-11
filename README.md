# Proof of Concept - POAM Automation

- [ ] Python Script to Pull AWS Inspector Results
- [ ] Python Script to Push AWS Inspector Results to POAM
- [X] Python Script to Merge Tenable Audit Scans and Vulnerability Scans
- [X] Python Script that updates a POAM using Excel in Git Repo.
	- Still getting errors 	
- [ ] Python script that updates a POAM using the Google Sheets API, running from a GitHub Action.
- [ ] Python Script 




-----------------

# Scripts

## merge.py 

**Constants**

- `DIRECTORY`: Specifies the folder where the CSV files are stored.
- `OUTPUT_FILE`: Location where the merged CSV will be saved.
- `FILE_EXTENSION`: Specifies that only .csv files should be processed.

**Functions**

1. `load_and_label_csv(file_path, scan_type)`:
    - This function loads a CSV file into a Pandas DataFrame and adds a column to label the type of scan (STIG or vulnerability).
    - If there’s an issue reading the file, it catches the error and returns an empty DataFrame.
2. `identify_scan_type(file_name)`:
   - Determines the scan type based on the file name using regular expressions. If the name contains “AWS_CIS” or “STIG,” it’s labeled as “STIG Scan”; otherwise, it’s labeled as “Vulnerability Scan.”
3. `split_multi_value_column(df, column_name)`:
   - Some rows in the CSV might have multiple values in a single cell (e.g., newline-separated). This function splits such values into separate rows.
   - This ensures each value in the specified column (“Weakness Description”) appears in its own row.
4. `merge_csv_files(directory)`:
   - This is the core function that merges all CSV files from the given directory.
   - It iterates over all files, identifies their scan type, and loads them using the previous functions.
   - If a file has a “Weakness Description” column, it splits any multi-value cells.
   - Finally, it concatenates all DataFrames into one, and rearranges the columns to have “Scan_Type” at the front.
5. `save_to_csv(df, output_file)`:
   - Saves the merged DataFrame to the specified CSV file.
  
**Main Execution (if __name__ == "__main__":)**
- This section calls the merge_csv_files function to process the CSVs and then saves the result to OUTPUT_FILE.
- A message is printed once the CSV is successfully saved.




## paom-update-repo.py

**File Paths**
- `merged_vulnerability_data_path`: Path to the CSV file containing the merged vulnerability data.
- `poam_excel_path`: Path to the Excel file containing the POAM data.

**Step-by-Step Breakdown**

1. **Load the Data:**
   - `merged_df`: Loads the vulnerability data from the CSV file while skipping the first two rows (likely to skip metadata or header information).
   - `poam_df`: Loads the POAM data from the Excel file using the openpyxl engine, again skipping the first two rows.
2. **Debugging:**
   - `print(merged_df.columns)`: Prints the column names of the vulnerability data to check if they match expected values for mapping.
   - `print(merged_df.head())`: Displays the first few rows of the merged vulnerability data for inspection.
3. **Mapping:**
   - The mapping dictionary defines how columns in the Tenable vulnerability data `(merged_df)` should map to the POAM `(poam_df)`.
   - For example, the “Plugin” column in the vulnerability data corresponds to the “Weakness Source Identifier” in the POAM.
4. **Check for New Vulnerabilities:**
   - The script iterates over each row of the merged vulnerability data.
   - For each row, it checks if the combination of “Plugin ID” and “Host” from the vulnerability data exists in the POAM.
   - If this combination doesn’t exist in the POAM (i.e., it’s a new vulnerability), it finds the first empty row in the POAM and adds the new vulnerability.
   - It populates the row based on the predefined column mappings (mapping).
5. **Handling Errors:**
   - KeyError: If any of the expected columns (like ‘Plugin’ or ‘Host’) are missing, it catches the error and prints a message.
   - IndexError: If there are no empty rows left in the POAM to add new vulnerabilities, it stops and prints a message.
6. **Save the Updated POAM:**
   - The updated POAM is saved to a new Excel file, `updated_poam_excel_path`, using the `openpyxl` engine.


## paom-update-gsheet.py

1. **Imports**:
   - The code uses `pandas` to handle CSV data and `gspread` to interact with Google Sheets.
   - `ServiceAccountCredentials` is used to authenticate with Google APIs via a service account.
2. **Authentication**:
   - The `scope` defines the permissions needed for accessing Google Sheets and Google Drive.
   - Credentials are loaded from a JSON file (`creds.json`), which contains the service account details.
3. **Accessing Google Sheets**:
   - The code opens a Google Sheet using the `sheet ID`.
   - It accesses the first worksheet (`get_worksheet(0)`), assuming that’s where the data needs to be updated.
4. **Loading CSV Data**:
   - A CSV file (`merged_vulnerability_data.csv`) is loaded into a Pandas DataFrame for easy manipulation.
5. **Converting Data**:
   - The DataFrame is converted into a list of lists (`df.values.tolist()`) so it can be pushed into Google Sheets.
6. **Updating Google Sheets**:
   - The `update` function uploads the list data to the Google Sheet, starting from cell A1.
