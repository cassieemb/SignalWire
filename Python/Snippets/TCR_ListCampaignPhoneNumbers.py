import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

# assign client variables
SpaceURL = ''
projectID = ""
authToken = ""
campaignSID = ""
host = f"https://{SpaceURL}"


# define URL for API Endpoint
url = f"https://{SpaceURL}/api/relay/rest/registry/beta/campaigns/{campaignSID}/numbers?page_size=1000"
payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload, auth=HTTPBasicAuth(projectID, authToken)).json()
campaignNumbers = response['data']

while "next" in response['links'].keys():
     response = requests.get(host + response['links']['next'], auth=HTTPBasicAuth(projectID, authToken)).json()
     campaignNumbers.extend(response['data'])
print(f"There are {len(campaignNumbers)} total numbers in campaign {campaignSID}.")

# Sets up an empty array
d = []

# loop through numbers
for number in campaignNumbers:
    d.append((number['phone_number']['number'], number['state'], number['created_at']))

df = pd.DataFrame(d, columns=('Phone Number', 'State', 'Date Added'))
print(df.to_string())

# Exports dataframe to csv, index=False turns off the indexing for each row
df.to_csv('CampaignNumbers.csv', index=False, encoding='utf-8')