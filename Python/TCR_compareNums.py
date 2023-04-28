from signalwire.rest import Client as signalwire_client
import csv
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# define your variables here to reuse throughout code
SpaceURL = os.getenv("SPACE_URL")
projectID = os.getenv("PROJECT_ID")
authToken = os.getenv("AUTH_TOKEN")
PathToCSV = 'CampaignNumbers.csv'

# Replace project ID, auth token, and space URL
client = signalwire_client(projectID, authToken, signalwire_space_url=SpaceURL)

# List and print all numbers on account
incoming_phone_numbers = client.incoming_phone_numbers.list()
print("Total Numbers -- " + str(len(incoming_phone_numbers)))

# create empty array to store numbers that are already registered
results = []
unregistered = []

# Open CSV file with registered numbers
with open(PathToCSV, 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    # Change to E164 format if it's not already in that format
    for row in reader:
        if "+" not in row[0]:
            results.append("+" + row[0])
        else:
            results.append(row[0])


# Loop through all account numbers, add number to list if unregistered
for record in incoming_phone_numbers:
    if record.phone_number in results:
        continue
    else:
        print('unregistered number --' + record.phone_number)
        unregistered.append(record.phone_number)

# Puts message log array into dataframe with headers for easier reading.
df = pd.DataFrame(unregistered, columns=['Phone Number'])
df.to_csv('UnregisteredNumbers.csv', index=False, encoding='utf-8')
