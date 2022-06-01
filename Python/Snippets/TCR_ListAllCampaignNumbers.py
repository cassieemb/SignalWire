import requests
from requests.auth import HTTPBasicAuth
from signalwire.rest import Client as signalwire_client
import pandas as pd

# define your variables here to reuse throughout code
SpaceURL = 'example.signalwire.com'
projectID = ""
authToken = ""
host = f"https://{SpaceURL}"
all_campaign_numbers = []

# Replace project ID, auth token, and space URL
client = signalwire_client(projectID, authToken, signalwire_space_url=SpaceURL)


# list all of our brands
response = requests.get(f"https://{SpaceURL}/api/relay/rest/registry/beta/brands",
                             headers={
                                 "Accept": "application/json",
                                 "Content-Type": "application/json"},
                             auth=HTTPBasicAuth(projectID, authToken)).json()
brands = response['data']

while "next" in response['links'].keys():
     response = requests.get(host + response['links']['next'], auth=HTTPBasicAuth(projectID, authToken)).json()
     brands.extend(response['data'])

print(f"You have {len(brands)} brands!")

# loop through each brand and check for its campaigns
for brand in brands:
    brand_sid = brand['id']
    brand_ID = brand['csp_brand_reference']

    # list campaigns for this brand
    response = requests.get(f"https://{SpaceURL}/api/relay/rest/registry/beta/brands/{brand_sid}/campaigns",
                            headers={
                                "Accept": "application/json",
                                "Content-Type": "application/json"},
                            auth=HTTPBasicAuth(projectID, authToken)).json()

    # view campaigns
    campaigns = response['data']

    # add pagination
    while "next" in response['links'].keys():
        response = requests.get(host + response['links']['next'], auth=HTTPBasicAuth(projectID, authToken)).json()
        campaigns.extend(response['data'])

    print(f"You have {len(campaigns)} campaigns in the brand {brand_ID}!")

    for campaign in campaigns:
        campaignSID = campaign['id']
        campaignID = campaign['csp_campaign_reference']
        campaignName = campaign['name']

        # loop through campaigns and list campaign numbers
        url = f"https://{SpaceURL}/api/relay/rest/registry/beta/campaigns/{campaignSID}/numbers?page_size=1000"
        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload,
                                    auth=HTTPBasicAuth(projectID, authToken)).json()
        campaignNumbers = response['data']

        while "next" in response['links'].keys():
            response = requests.get(host + response['links']['next'], auth=HTTPBasicAuth(projectID, authToken)).json()
            campaignNumbers.extend(response['data'])

        print(f"There are {len(campaignNumbers)} total numbers in campaign {campaignID}.")

        # loop through each campaign number
        for number in campaignNumbers:
            numberID = number['phone_number']['id']
            tn = number['phone_number']['number']
            numberState = number['state']
            addToCampaignDate =number['created_at']

            all_campaign_numbers.append([brand_sid, brand_ID, campaignSID, campaignID, numberID, tn, numberState, addToCampaignDate])


# create dataframe
df = pd.DataFrame(all_campaign_numbers, columns=('Brand SID', 'Brand ID', 'Campaign SID', 'Campaign ID', 'Number SID', 'Number', 'Number State', 'Date Added to Campaign'))
print(df.to_string())

df.to_csv('AllSpaceCampaigns.csv', index=False, encoding='utf-8')