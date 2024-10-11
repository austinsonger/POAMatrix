/*
PROJECT NAME: AWS Inspector Findings into Google Drive + POAM
GITHUB URL: https://github.com/CirrusMD/Automation-AWS-Inspector-Findings

- Fetching AWS Data: fetchAwsInspectorResults fetches the data from AWS Lambda via an API Gateway endpoint.
- Processing Data: processLambdaData processes the fetched data. Customize this function based on our data processing needs.
- CSV Conversion: convertToCsv converts the processed data into CSV format. It creates a string representing the CSV data.
- Google Drive Update: updateGoogleDrive checks if a file with a given name exists in a specific Google Drive folder. If it exists, the script updates the file with new data; otherwise, it creates a new file.
- Main Function: main orchestrates the entire process by calling the above functions in sequence.
- Scheduling: setupTrigger sets up an automated trigger to run the main function periodically.
*/

// Fetch results from AWS Inspector via AWS Lambda and API Gateway
// TO-DO: Replace 'YOUR_AWS_API_GATEWAY_ENDPOINT' with your actual AWS
function fetchAwsInspectorResults() {
  var url = '[AWS_API_GATEWAY_ENDPOINT]';
  var response = UrlFetchApp.fetch(url);
  var data = JSON.parse(response.getContentText());
  return data;
}

// TO-DO: Customize this function to process our data as required.
function processLambdaData(data) {
  // TO-DO: Return data as is or apply transformations
  return data;
}

// Convert the processed data to CSV format
function convertToCsv(data) {
  var csvData = '';
  var keys = Object.keys(data[0]);

  // Add header row
  csvData += keys.join(',') + '\n';

  // Add data rows
  data.forEach(function(row) {
    keys.forEach(function(key, index) {
      if (index > 0) csvData += ',';
      csvData += JSON.stringify(row[key]);
    });
    csvData += '\n';
  });

  return csvData;
}

// TO-DO: Replace 'FolderName' with the actual name of the Google Drive folder.
function updateGoogleDrive(csvData) {
  var fileName = 'AWS_Inspector_Results.csv';
  var folder = DriveApp.getFoldersByName('FolderName').next();
  var files = folder.getFilesByName(fileName);
  var file;

  if (files.hasNext()) {
    file = files.next();
    file.setContent(csvData);
  } else {
    file = folder.createFile(fileName, csvData, MimeType.PLAIN_TEXT);
  }
}

// Main function to orchestrate the workflow
function main() {
  var awsData = fetchAwsInspectorResults();
  var processedData = processLambdaData(awsData);
  var csvData = convertToCsv(processedData);
  updateGoogleDrive(csvData);
}

// Time-driven trigger
function setupTrigger() {
  ScriptApp.newTrigger('main')
    .timeBased()
    .everyDays(25) // Adjust if Needed
    .create();
}
