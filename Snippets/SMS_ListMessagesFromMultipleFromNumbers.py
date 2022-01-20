from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd

client = signalwire_client("ProjectID", "AuthToken",
                           signalwire_space_url='SpaceURL.signalwire.com')

from_numbers = ["+18593986322", "+18592950575"]
d = []

for number in from_numbers:
    messages = client.messages.list(from_=number, date_sent_after=(datetime(2021, 11, 30)))
    for record in messages:
        d.append((record.from_, record.to, record.date_sent, record.status, record.sid, record.body, record.error_message))


df = pd.DataFrame(d, columns=('From', 'To', 'Date', 'Status', 'MessageSID', 'Message Body', 'Error Message'))

print('dataframe')
print('\n')
print(df)

df.to_csv('CompanyName.csv', index=False, encoding='utf-8')