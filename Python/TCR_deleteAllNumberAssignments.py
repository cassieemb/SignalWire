import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

# define your variables here to reuse throughout code
SpaceURL = os.getenv("SPACE_URL")
projectID = os.getenv("PROJECT_ID")
authToken = os.getenv("AUTH_TOKEN")
campaignSID = "some-alphanumeric-string"
host = f"https://{SpaceURL}"

# List All Campaign Numbers
url = f"https://{SpaceURL}/api/relay/rest/registry/beta/campaigns/{campaignID}/numbers?page_size=1000"
payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload, auth=HTTPBasicAuth(projectID, authToken)).json()
campaignNumbers = response['data']

while "next" in response['links'].keys():
     response = requests.get(host + response['links']['next'], auth=HTTPBasicAuth(projectID, authToken)).json()
     campaignNumbers.extend(response['data'])

# loop through numbers and call delete number function on each
for number in campaignNumbers:
    tn = number['phone_number']['number']
    numberSID = number['phone_number']['id']
    assignmentSID = number['id']

    try:
        url = f"https://{SpaceURL}/api/relay/rest/registry/beta/numbers/{assignmentSID}"
        payload = {}
        headers = {}
        response = requests.request("DELETE", url, headers=headers, data=payload, auth=HTTPBasicAuth(projectID, authToken))
        if response.ok:
            print(f"{tn} successfully deleted")
        else:
            print(f"{response.status_code} {response.text}. {tn} not deleted.")

    except Exception as e:
        print(f"Error: {str(e)}")











