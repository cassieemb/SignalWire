from signalwire.rest import Client as signalwire_client
import csv
import requests
from requests.auth import HTTPBasicAuth

# define your variables here so they don't need to be hardcoded
SpaceURL = 'YourSpace.signalwire.com'
ProjectID = "Some-Alphanumeric-String"
AuthToken = 'Some-Alphanumeric-String'
WebhookPath = 'https://example.com/message_handler'
PathToCSV = 'Path-To-CSV-On-Your-Computer'

# Replace project ID, auth token, and space URL
client = signalwire_client(ProjectID, AuthToken, signalwire_space_url=SpaceURL)

# List and print all numbers on account
incoming_phone_numbers = client.incoming_phone_numbers.list()
print("Total Numbers -- " + str(len(incoming_phone_numbers)))

# create empty array to store numbers that need webhooks updated
results = []

# Open CSV file with numbers whose webhooks you want to update, replace with file path and file
with open(PathToCSV, 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    # Change to E164 format if it's not already in that format
    for row in reader:
        if "+" not in row[0]:
            results.append("+" + row[0])
        else:
            results.append(row[0])
print(results)

# Loop through all account numbers, if number exists in Results array, print to console and update webhook
for record in incoming_phone_numbers:
    if record.phone_number in results:
        print("update number -- " + record.phone_number)
        response = requests.put('https://+SpaceURL+/api/relay/rest/phone_numbers/' + record.sid,
                                params={'call_handler': 'laml_webhooks',
                                        'message_request_url': WebhookPath}
                                , auth=HTTPBasicAuth(ProjectID, AuthToken))
        print(response)
