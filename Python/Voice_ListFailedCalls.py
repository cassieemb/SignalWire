from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

client = signalwire_client(os.getenv("PROJECT_ID"), os.getenv("AUTH_TOKEN"),
                           signalwire_space_url=os.getenv("SPACE_URL"))

# list calls filtered by parameters such as date range, from number, to number, etc
calls = client.calls.list(start_time_after=datetime(2021, 0o4, 29))


# Sets up an empty array
d = []

# Appends all data from calls with status failed into an array
for record in calls:
    if record.status == 'failed':
        d.append((record.from_formatted, record.to_formatted, record.start_time, record.sid, record.duration))

print(d)

# Puts call log array into dataframe with headers for easier reading.
df = pd.DataFrame(d, columns=('From', 'To', 'Date', 'CallSID', 'Duration in Seconds'))

print('dataframe')
print('\n')
print(df)

# Exports dataframe to csv, index=False turns off the indexing for each row
df.to_csv('FailedCalls.csv', index=False, encoding='utf-8')
