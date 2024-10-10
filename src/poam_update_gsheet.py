import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope and credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)  # The temp creds.json file
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open_by_key("your-google-sheet-id")  # Replace with your Google Sheet ID
worksheet = sheet.get_worksheet(0)  # Assuming you're working with the first sheet

# Load the CSV file
df = pd.read_csv('output/merged_vulnerability_data.csv')

# Convert the DataFrame to a list of lists for Google Sheets update
data = df.values.tolist()

# Update the Google Sheet
worksheet.update("A1", data)  # Update the data starting from cell A1