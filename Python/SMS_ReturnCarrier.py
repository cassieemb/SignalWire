from datetime import datetime
from signalwire.rest import Client as signalwire_client
from requests.auth import HTTPBasicAuth
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

client = signalwire_client(os.getenv("PROJECT_ID"), os.getenv("AUTH_TOKEN"),
                           signalwire_space_url=os.getenv("SPACE_URL"))

# Create an array for each column in our final dataframe of wireless recipients
line_type_list = []
sms_enabled_number_list = []
line_carrier_list = []

messages = client.messages.list(date_sent_after=datetime(2021, 2, 17, 0, 0))
destination_numbers = []

# Appends all data from messages into an array
for record in messages:
    if record.direction == 'outbound-api':
        destination_numbers.append(record.to)

for i in destination_numbers:
    # iterate through each number
    url = f"https://{os.getenv('SPACE_URL')}/api/relay/rest/lookup/phone_number/{i}?include=carrier"
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload,
                                auth=HTTPBasicAuth(os.getenv("PROJECT_ID"), os.getenv("AUTH_TOKEN"))).json()

    # determine mobile type
    line_type = response['carrier']['linetype']
    # add details about confirmed mobiles to array
    if line_type == 'wireless':
        # Let the console know which numbers will be added to our dataframe
        print(i + ' is a wireless number')
        line_type_list.append(line_type)

        # track carriers
        line_carrier = response['carrier']['lec']
        line_carrier_list.append(line_carrier)

# Turn each of our columns into a complete data frame
final_dataframe = pd.DataFrame(({'Carrier': line_carrier_list}))

# Isolate the 'from' number column of our data frame and count the frequency of each unique occurrence
carrier_table = (final_dataframe['Carrier'].value_counts()).reset_index()

# Take only the 10 most popular from destinations and add labels to our data frame
carrier_table.columns = ['From_Destination', 'Frequency']
carrier_table.to_csv('MessagesByCarrier.csv', index=False, encoding='utf-8')
