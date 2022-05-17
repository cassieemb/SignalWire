from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd

client = signalwire_client("", "",
                           signalwire_space_url='EXAMPLE.signalwire.com')

# Lists messages from/to a particular number within a specific date range or with a specific status
messages = client.messages.list(date_sent=datetime(2022, 4, 27))

# Sets up an empty array
d = []
c = []

# Appends all data from messages into an array
for record in messages:
    d.append((record.from_, record.to, record.date_sent, record.status, record.sid, record.error_message))
    c.append(record.status)

print(d)

# Puts message log array into dataframe with headers for easier reading.
df = pd.DataFrame(d, columns=('From', 'To', 'Date', 'Status', 'MessageSID', 'Error Message'))

print('dataframe')
print('\n')
print(df.to_string())

# Exports dataframe to csv, index=False turns off the indexing for each row
df.to_csv('Messages.csv', index=False, encoding='utf-8')

# Transfer Variables to Int
num_sent = int(c.count("sent"))
num_received = int(c.count("received"))
num_delivered = int(c.count("delivered"))
num_undelivered = int(c.count("undelivered"))
num_queued = int(c.count("queued"))

# Calculate Total Number Outbound Messages
num_outbound_messages = num_sent + num_delivered + num_undelivered
num_inbound_messages = num_received

# Make it look Pretty
print("You Have " + str(num_sent) + " Sent Messages")
print("You Have " + str(num_delivered) + " Delivered Messages")
print("You Have " + str(num_undelivered) + " Undelivered Messages")
print("\nYou Also Have " + str(num_received) + " Received Messages")
print(f"You have {str(num_queued)} queued messages.")
