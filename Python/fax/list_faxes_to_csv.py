from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv('../../.env')

client = signalwire_client(os.getenv("PROJECT_ID"), os.getenv("AUTH_TOKEN"),
                           signalwire_space_url=os.getenv("SPACE_URL"))

faxes = client.fax.faxes.list(
    # to='+1xxxxxxxxxx',
    # from_='+1xxxxxxxxxx',
    date_created_after=datetime(2020, 0o3, 0o1, 17, 0o7, 0),
    date_created_on_or_before=datetime(2023, 0o4, 1, 0, 0, 0),
)

# Sets up an empty array
d = []

# Appends all data from calls into an array
for record in faxes:
    d.append((record.from_, record.to, record.date_created, record.status, record.sid))

# Puts fax log array into dataframe with headers for easier reading.
df = pd.DataFrame(d, columns=('From', 'To', 'Date', 'Status', 'FaxSID'))

# Exports dataframe to csv, index=False turns off the indexing for each row
df.to_csv('faxes.csv', index=False, encoding='utf-8')
