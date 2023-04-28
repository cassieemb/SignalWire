from signalwire.rest import Client as signalwire_client
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# define your variables here to reuse throughout code
SpaceURL = os.getenv("SPACE_URL")
ProjectID = os.getenv("PROJECT_ID")
AuthToken = os.getenv("AUTH_TOKEN")
WebhookPath = 'https://example.com/message_handler'
CampaignSID = "some-alphanumeric-string"
numberToPurchase = '+1206xxxxxxx' # no dashes, parentheses, or spaces, make sure to include country code

# Replace project ID, auth token, and space URL
client = signalwire_client(ProjectID, AuthToken, signalwire_space_url=SpaceURL)

# format number in e164 if necessary
formattedNumber = "+" + numberToPurchase if "+" not in numberToPurchase else numberToPurchase


# buy phone number
response = requests.post(f"https://{SpaceURL}/api/relay/rest/phone_numbers",
                         headers = { "Accept": "application/json",
                             "Content-Type": "application/json"},
                         json = {"number": formattedNumber},
                         auth=HTTPBasicAuth(ProjectID, AuthToken))
sid = response.json()['id']
purchaseDate = response.json()['created_at']
print(response.text)


# assign webhook
response = requests.put(f"https://{SpaceURL}/api/relay/rest/phone_numbers/{sid}",
                               params={'call_handler': 'laml_webhooks',
                                        'message_request_url': WebhookPath,
                                        'name': 'Number Name'},
                         auth=HTTPBasicAuth(ProjectID, AuthToken))
print(response.text)

# assign campaign
response = requests.post(f"https://{SpaceURL}/api/relay/rest/registry/beta/campaigns/{CampaignSID}/orders",
                         json = {"phone_numbers": [formattedNumber]},
                         headers = {
                            "Accept": "application/json",
                               "Content-Type": "application/json"},
                         auth=HTTPBasicAuth(ProjectID, AuthToken))
print(response.text)

# retrieve campaign
response = requests.get(f"https://{SpaceURL}/api/relay/rest/registry/beta/campaigns/{CampaignSID}",
                         headers = {"Accept": "application/json"},
                         auth=HTTPBasicAuth(ProjectID, AuthToken))
campaignRef = response.json()['csp_campaign_reference']

# read in csv and append new row with number, campaign, webhook, purchase date
numberAssociations = pd.read_csv('src/NumberAssociations.csv')
numberAssociations.loc[len(numberAssociations.index)] = [formattedNumber, campaignRef, CampaignSID, WebhookPath, purchaseDate]
numberAssociations.to_csv('src/NumberAssociations.csv', index=None)

