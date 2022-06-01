from signalwire.rest import Client as signalwire_client
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import csv

# define your variables here to reuse throughout code
SpaceURL = '.signalwire.com'
projectID = ""
authToken = ""
campaignSID = ""
PathToCSV = 'UnregisteredNumbers.csv'
results = []

# Replace project ID, auth token, and space URL
client = signalwire_client(projectID, authToken, signalwire_space_url=SpaceURL)


# Open CSV file with registered numbers
with open(PathToCSV, 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    # Change to E164 format if it's not already in that format
    for row in reader:
        if "+" not in row[0]:
            results.append("+" + row[0])
        else:
            results.append(row[0])

for result in results:
    try:
         response = requests.post(f"https://{SpaceURL}/api/relay/rest/registry/beta/campaigns/{campaignSID}/orders",
                          json = {"phone_numbers": [result]},
                          headers = {
                             "Accept": "application/json",
                                "Content-Type": "application/json"},
                          auth=HTTPBasicAuth(projectID, authToken))
         if response.ok:
             print(f"{result} added to campaign")
         else:
             print(f"{response.status_code} {response.text}. {result} not added to campaign.")

    except Exception as e:
         print(f"Error: {str(e)}")


