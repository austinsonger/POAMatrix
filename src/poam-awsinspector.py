import json
import boto3
import logging
from botocore.exceptions import ClientError
# TO-DO: 
# 1. IAM Role and Permissions
# -- inspector:ListFindings - https://docs.aws.amazon.com/inspector/v2/APIReference/API_ListFindings.html
# -- inspector:DescribeFindings - https://docs.aws.amazon.com/inspector/v1/APIReference/API_DescribeFindings.html

def lambda_handler(event, context):
    client = boto3.client('inspector')
    
    # Fetch AWS Inspector findings or reports
    findings = client.list_findings() # TO-DO: Additional processing or filters???

    # TO-DO:
    # - Process and format the data
    # - Extracting specific details from each finding
    # - Converts the response to JSON
    findings_data = json.dumps(findings) 

    
    # TO-DO: Log the processed data (or store/send it as needed)   
    
    
    # Return the processed data
    return {
        'statusCode': 200,
        'body': findings_data
    }
