from datetime import datetime
from signalwire.rest import Client as signalwire_client
import base64
import requests
import pandas as pd

# ENTER AUTHENTICATION
space = 'contactmeasap21.signalwire.com'
Project_ID = '6b9eb3ca-4565-4e4b-b404-dc30b87a61b5'
API_Token = 'PT2be10d625449d7759857a2c9e46f41a154bcc966afacb9f0'

# Create an array for each column in our final dataframe of wireless recipients
line_type_list =[]
sms_enabled_number_list=[]
line_carrier_list =[]

client = signalwire_client(Project_ID, API_Token,signalwire_space_url=space)

# For our Relay-Rest APIs we will use a base64 encoded string of your projectID and API Token
base_64_token = Project_ID + ':' + API_Token
message_bytes = base_64_token.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base_64_token = base64_bytes.decode('ascii')

# The Number Lookup APIs are Relay-Rest so we must make an http request to the end points
# and declare what content to accept. We must also declare the content type and our Authorization Token which is base64 encoded
headers = {"Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "Basic "+ base_64_token}

messages = client.messages.list(date_sent=datetime(2022, 2, 17, 0, 0))
destination_numbers = []

# Appends all data from messages into an array
for record in messages:
    if record.direction == 'outbound-api':
        destination_numbers.append((record.to))


for i in destination_numbers:
    # Declare the url for our Number Dip API this will iterate through each number we are requesting to lookup
    number_lookup_url= "https://" + space + '/api/relay/rest/lookup/phone_number/' + i + '?include=carrier'
    # Make the complete API request for our Number Dip API
    number_lookup_API_Request = requests.request("GET", number_lookup_url, headers=headers)
    # Read the response from the API by accessing the json that was returned
    number_assignment_json = number_lookup_API_Request.json()
    # Find the type of number, whether landline or wireless
    line_type = number_assignment_json['carrier']['linetype']
    # If the number is sms enabled, we will append our dataframe with it's e164 format, the location and the type of number
    if line_type == 'wireless':
        # Let the console know which numbers will be added to our dataframe
        print(i + ' is a wireless number')
        line_type_list.append(line_type)
        # Create a list of the carriers of each number that is wireless enabled. This list will become a column in our final dataframe
        line_carrier = number_assignment_json['carrier']['lec']
        line_carrier_list.append(line_carrier)
    else:
        # Let the console know which numbers will NOT be added to our dataframe
        print(i + ' is NOT a wireless number')
# Turn each of our columns into a complete data frame
final_dataframe= pd.DataFrame(({'Carrier': line_carrier_list}))
# Isolate the 'from' number column of our data frame and count the frequency of each unique occurance
carrier_table = (final_dataframe['Carrier'].value_counts()).reset_index()
# Take only the 10 most popular from destinations and add labels to our data frame
carrier_table.columns = ['From_Destination', 'Frequency']
carrier_table.to_csv('Contact_Me_ASAP.csv', index=False, encoding='utf-8')