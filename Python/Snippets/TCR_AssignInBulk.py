import requests
from requests.auth import HTTPBasicAuth
import csv

# define your variables here to reuse throughout code
SpaceURL = '.signalwire.com'
projectID = ""
authToken = ""
campaignSID = ""
PathToCSV = 'UnregisteredNumbers.csv'
results = []

# Open CSV file with unregistered numbers
with open(PathToCSV, 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    # Change to E164 format if it's not already in that format
    for row in reader:
        if "+" not in row[0]:
            results.append("+" + row[0])
        else:
            results.append(row[0])

for result in results:
    try:
        response = requests.post(f"https://{SpaceURL}/api/relay/rest/registry/beta/campaigns/{campaignSID}/orders",
                                 json={"phone_numbers": [result]},
                                 headers={
                                     "Accept": "application/json",
                                     "Content-Type": "application/json"},
                                 auth=HTTPBasicAuth(projectID, authToken))
        if response.ok:
            print(f"{result} added to campaign")
        else:
            print(f"{response.status_code} {response.text}. {result} not added to campaign.")

    except Exception as e:
        print(f"Error: {str(e)}")
