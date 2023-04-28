import pandas as pd
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

# define URL for API Endpoint
url = f"https://{SpaceURL}/api/relay/rest/registry/beta/campaigns/{campaignSID}/numbers"
payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload, auth=HTTPBasicAuth(projectID, authToken)).json()
campaignNumbers = response['data']

while "next" in response['links'].keys():
    response = requests.get(host + response['links']['next'], auth=HTTPBasicAuth(projectID, authToken)).json()
    campaignNumbers.extend(response['data'])

print(f"There are {len(campaignNumbers)} total numbers in campaign {campaignSID}.")

# Sets up an empty array
d = []

# assigned numbers version

# loop through numbers
for number in campaignNumbers:
    print(number)
    d.append((number['phone_number']['number'], number['state'], number['updated_at']))

df = pd.DataFrame(d, columns=('Phone Number', 'State', 'Last Updated Date'))
print(df.to_string())

# Exports dataframe to csv, index=False turns off the indexing for each row
df.to_csv('CampaignNumbers.csv', index=False, encoding='utf-8')

'''
# campaign assignments version

# loop through numbers
for number in campaignNumbers:
    print(number)
    d.append((number['id'], number['state'], number['created_at'], number['updated_at']))

df = pd.DataFrame(d, columns=('Assignment ID', 'State', 'Created Date', 'Last Updated Date'))
print(df.to_string())

# Exports dataframe to csv, index=False turns off the indexing for each row
df.to_csv('CampaignNumbersAssignments.csv', index=False, encoding='utf-8')
'''
