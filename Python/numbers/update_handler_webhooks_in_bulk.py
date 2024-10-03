from signalwire.rest import Client as signalwire_client
import csv
import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv('../../.env')

WebhookPath = 'https://example.com/message_handler'
PathToCSV = 'Path-To-CSV-On-Your-Computer'

client = signalwire_client(os.getenv("PROJECT_ID"), os.getenv("AUTH_TOKEN"),
                           signalwire_space_url=os.getenv("SPACE_URL"))

# List and print all numbers on account
incoming_phone_numbers = client.incoming_phone_numbers.list()
print("Total Numbers -- " + str(len(incoming_phone_numbers)))

# create empty array to store numbers that need webhooks updated
results = []

# Open CSV file with numbers whose webhooks you want to update, replace with file path and file
with open(PathToCSV, 'r', encoding='utf-8-sig') as csv_file:
    reader = csv.reader(csv_file)
    # Change to E164 format if it's not already in that format
    for row in reader:
        if "+" not in row[0]:
            results.append("+" + row[0])
        else:
            results.append(row[0])

# Loop through all account numbers, if number exists in Results array, print to console and update webhook
for record in incoming_phone_numbers:
    if record.phone_number in results:
        print(f"update number -- {record.phone_number}")
        response = requests.put(
            f"https://{os.getenv('SPACE_URL')}/api/relay/rest/phone_numbers/{record.sid}",
            params={'call_handler': 'laml_webhooks', 'message_request_url': WebhookPath},
            auth=HTTPBasicAuth(os.getenv("PROJECT_ID"), os.getenv("AUTH_TOKEN")))
        print(response)
