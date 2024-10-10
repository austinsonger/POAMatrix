#!/bin/bash

# Constants
DIRECTORY="./scans_directory"  # Replace with your directory path
OUTPUT_FILE="merged_vulnerability_data.csv"
FILE_EXTENSION="*.csv"

# Function to identify scan type based on regex
identify_scan_type() {
    file_name="$1"
    if [[ "$file_name" =~ AWS_CIS|STIG ]]; then
        echo "STIG Scan"
    else
        echo "Vulnerability Scan"
    fi
}

# Function to merge CSV files
merge_csv_files() {
    # Check if output file exists and delete it to avoid appending to old data
    [ -f "$OUTPUT_FILE" ] && rm "$OUTPUT_FILE"

    # Find all CSV files in the directory
    csv_files=$(find "$DIRECTORY" -type f -name "$FILE_EXTENSION")

    # Add the header from the first CSV file
    first_file=$(echo "$csv_files" | head -n 1)
    echo "Scan_Type,$(head -n 1 "$first_file")" > "$OUTPUT_FILE"

    # Loop through each file and append its contents
    for file in $csv_files; do
        scan_type=$(identify_scan_type "$file")
        # Append file contents with Scan_Type added as the first column
        # Handling for special characters and quotes with CSV
        tail -n +2 "$file" | sed -e "s/^/\"$scan_type\",/" >> "$OUTPUT_FILE"
    done

    echo "Merged CSV saved to $OUTPUT_FILE"
}

# Run the function
merge_csv_files