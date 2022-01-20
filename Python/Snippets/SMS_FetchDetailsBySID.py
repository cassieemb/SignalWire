from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd
import csv

client = signalwire_client("ProjectID", "AuthToken",
                           signalwire_space_url='spaceURL.signalwire.com')

# list all messages on account within last 48 hours
messages = client.messages.list(date_sent_after=datetime(2021, 10, 10, 0, 0), date_sent_before=datetime(2021, 10, 12, 0, 0))

# Sets up an empty array for the csv and an empty array to store data
results = []
undeliveredData = []

# open CSV with messages to get more data about
with open("textline_message_failures.csv", 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
print(results)

# loop through messages and if any match results array, fetch additional data
for record in messages:
    if record.sid in results:
        message = client.messages(record.sid).fetch()
        undeliveredData.append((record.from_, record.to, record.date_sent))


df = pd.DataFrame(undeliveredData, columns=('From', 'To', 'Date'))

print('Completed Dataframe')
print('\n')
print(df)

# Exports dataframe to csv, index=False turns off the indexing for each row
df.to_csv('messages.csv', index=False, encoding='utf-8')