from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

client = signalwire_client(os.getenv("PROJECT_ID"), os.getenv("AUTH_TOKEN"),
                           signalwire_space_url=os.getenv("SPACE_URL"))


calls = client.calls.list(
    start_time_after=datetime(2021, 0o4, 29),
    start_time_before=datetime(2024, 0o1, 27),
    from_=os.getenv("FROM_NUMBER"),

)

# Sets up an empty array
d = []

# Appends all data from calls into an array
for record in calls:
    d.append((record.from_formatted, record.to_formatted, record.start_time, record.status, record.sid))

print(d)

# # Puts call log array into dataframe with headers for easier reading.
df = pd.DataFrame(d, columns=('From', 'To', 'Date', 'Status', 'CallSID'))

print('dataframe')
print('\n')
print(df)

# # Exports dataframe to csv, index=False turns off the indexing for each row
df.to_csv('calls.csv', index=False, encoding='utf-8')
