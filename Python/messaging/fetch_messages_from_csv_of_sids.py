from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd
import csv
import os
from dotenv import load_dotenv

load_dotenv('../../.env')

client = signalwire_client(os.getenv("PROJECT_ID"), os.getenv("AUTH_TOKEN"),
                           signalwire_space_url=os.getenv("SPACE_URL"))

# list all messages on account within date range
messages = client.messages.list(date_sent_after=datetime(2021, 10, 10, 0, 0),
                                date_sent_before=datetime(2021, 10, 12, 0, 0))

# Set up an empty array for the csv and an empty array to store SIDs
results = []
undeliveredData = []

# open CSV with messages to investigate
with open("message_failures_doc.csv", 'r', encoding='utf-8-sig') as csv_file:
    reader = csv.reader(csv_file)

# loop through messages and if any match results array, fetch additional data
for record in messages:
    if record.sid in results:
        message = client.messages(record.sid).fetch()
        undeliveredData.append((record.from_, record.to, record.date_sent))

df = pd.DataFrame(undeliveredData, columns=('From', 'To', 'Date'))

# Exports dataframe to csv, index=False turns off the indexing for each row
df.to_csv('undelivered_messages.csv', index=False, encoding='utf-8')
