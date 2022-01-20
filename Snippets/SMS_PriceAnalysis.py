from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd

client = signalwire_client("ProjectID", "AuthToken", signalwire_space_url='YourSpace.signalwire.com')

# filter using date_sent_after and date_sent_before to get a time range to filter messages by
messages = client.messages.list(date_sent_after=datetime(2021, 10, 1), date_sent_before=datetime(2021, 10, 31))

d = []
status = []

for record in messages:
    d.append((record.from_, record.to, record.date_sent, record.sid, record.price, record.direction, record.status))
    status.append(record.status)

# categorize message status for all returned messages
total_sent=int(status.count("sent"))
total_received=int(status.count("received"))
total_delivered=int(status.count("delivered"))
total_undelivered=int(status.count("undelivered"))

# count how many are inbound vs outbound
num_outbound_messages = total_sent + total_delivered + total_undelivered
num_inbound_messages = total_received

# create dataframe and convert to CSV
df = pd.DataFrame(d, columns=('From', 'To', 'Date', 'MessageSID',  'Price', 'Message Direction', 'Message Status'))
print(df)
df.to_csv('Messages.csv', index=False, encoding='utf-8')
print()

totalMess = len(df)
totalCost = df['Price'].sum()
formattedCost = "${:,.2f}".format(totalCost)

# print some quick summaries
print("You sent " + str(totalMess) + " total messages during your selected date range.")
print("The total cost of messages in your selected date range is approximately " + formattedCost + " USD.")
print("There were " + str(total_delivered) + " delivered messages and " + str(total_undelivered) +  " undelivered messages.")
print("There were " + str(num_inbound_messages) + " inbound messages and " + str(num_outbound_messages) + " outbound messages.")
