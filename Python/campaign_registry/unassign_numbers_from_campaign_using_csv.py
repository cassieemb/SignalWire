from requests.auth import HTTPBasicAuth
import requests
import csv
import os
from dotenv import load_dotenv

load_dotenv('../../.env')

# define your variables here to reuse throughout code
SpaceURL = os.getenv("SPACE_URL")
projectID = os.getenv("PROJECT_ID")
authToken = os.getenv("AUTH_TOKEN")
campaignID = "some-alphanumeric-string"
host = f"https://{SpaceURL}"
results = []

# read in CSV of numbers to delete
with open("Numbers.csv", 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)

    for row in reader:
        if "+" not in row[0]:
            results.append("+" + row[0])
        else:
            results.append(row[0])

# List All Campaign Numbers
url = f"https://{SpaceURL}/api/relay/rest/registry/beta/campaigns/{campaignID}/numbers?page_size=1000"
payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload, auth=HTTPBasicAuth(projectID, authToken)).json()
campaignNumbers = response['data']

while "next" in response['links'].keys():
    response = requests.get(host + response['links']['next'], auth=HTTPBasicAuth(projectID, authToken)).json()
    campaignNumbers.extend(response['data'])

# loop through numbers and call delete number function on each if tn in results
for number in campaignNumbers:
    tn = number['phone_number']['number']
    assignmentSID = number['id']
    if tn in results:

        try:
            url = f"https://{SpaceURL}/api/relay/rest/registry/beta/numbers/{assignmentSID}"
            payload = {}
            headers = {}
            response = requests.request("DELETE", url, headers=headers, data=payload,
                                        auth=HTTPBasicAuth(projectID, authToken))
            if response.ok:
                print(f"{tn} successfully deleted")
            else:
                print(f"{response.status_code} {response.text}. {tn} not deleted.")

        except Exception as e:
            print(f"Error: {str(e)}")
