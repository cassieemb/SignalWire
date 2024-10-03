import requests
import csv
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv('../../.env')

# define your variables here to reuse throughout code
SpaceURL = os.getenv("SPACE_URL")
projectID = os.getenv("PROJECT_ID")
authToken = os.getenv("AUTH_TOKEN")
host = f"https://{SpaceURL}"
campaigns = []

# read in campaigns CSV
with open("Campaigns.csv", 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for row in reader:
        campaigns.append(row[0])

# loop through campaigns and remove all numbers from each
for campaign in campaigns:
    print(f"Starting campaign {campaign} now")

    # List All Campaign Numbers
    url = f"https://{SpaceURL}/api/relay/rest/registry/beta/campaigns/{campaign}/numbers"
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload, auth=HTTPBasicAuth(projectID, authToken)).json()
    campaignNumbers = response['data']

    while "next" in response['links'].keys():
        response = requests.get(host + response['links']['next'], auth=HTTPBasicAuth(projectID, authToken)).json()
        campaignNumbers.extend(response['data'])

    # delete listed numbers
    for number in campaignNumbers:
        tn = number['phone_number']['number']
        numberSID = number['phone_number']['id']
        assignmentSID = number['id']

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
