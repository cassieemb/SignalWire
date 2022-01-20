from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd

client = signalwire_client("ProjectID", "AuthToken",
                           signalwire_space_url='example.signalwire.com')

# Start Time is a datetime object
# order for the arguments is Year, Month, Date, Hour, Minute, Seconds.
# Leave hour, minute, and seconds at 0
calls = client.calls.list(
    start_time_after=datetime(2021, 0o4, 29, 17, 0o7, 0),
    start_time_before=datetime(2021, 0o1, 27, 0, 0, 0),
    from_="+1888xxxxxxx",

)

# Appends all data from calls into an array
for record in calls:
    print((record.start_time, record.status, record.sid))

# # Sets up an empty array
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
