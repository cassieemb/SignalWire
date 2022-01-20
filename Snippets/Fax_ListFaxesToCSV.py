from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd

client = signalwire_client("ProjectID", "AuthToken",
                           signalwire_space_url='example.signalwire.com')

# Start Time is a datetime object
# order for the arguments is Year, Month, Date, Hour, Minute, Seconds.
# Leave hour, minute, and seconds at 0
faxes = client.fax.faxes.list(
    to='+18552147520',
    from_='+12252969340',
    date_created_after=datetime(2021, 0o3, 0o1, 17, 0o7, 0),
    date_created_on_or_before=datetime(2021, 0o4, 1, 0, 0, 0),

)

# Appends all data from calls into an array
for record in faxes:
    print((record.date_created, record.status, record.sid))

# # Sets up an empty array
d = []

# Appends all data from calls into an array
for record in faxes:
    d.append((record.from_, record.to, record.date_created, record.status, record.sid))

print(d)

# # Puts fax log array into dataframe with headers for easier reading.
df = pd.DataFrame(d, columns=('From', 'To', 'Date', 'Status', 'FaxSID'))

print('dataframe')
print('\n')
print(df)

# # Exports dataframe to csv, index=False turns off the indexing for each row
df.to_csv('faxes.csv', index=False, encoding='utf-8')
