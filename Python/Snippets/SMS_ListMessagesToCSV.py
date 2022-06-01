from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd

client = signalwire_client("ProjectID", "AuthToken",
                           signalwire_space_url='example.signalwire.com')

# Lists messages from/to a particular number within a specific date range or with a specific status
messages = client.messages.list(date_sent_after=datetime(2022, 2, 10))

# Sets up an empty array
d = []

# Appends all data from messages into an array
for record in messages:
    d.append((record.from_, record.to, record.date_sent, record.status, record.sid, record.error_message))

# Puts message log array into dataframe with headers for easier reading.
df = pd.DataFrame(d, columns=('From', 'To', 'Date', 'Status', 'MessageSID', 'Error Message'))

print('dataframe')
print('\n')
print(df.to_string())

# Exports dataframe to csv, index=False turns off the indexing for each row
df.to_csv('Messages.csv', index=False, encoding='utf-8')
