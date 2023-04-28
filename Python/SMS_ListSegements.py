from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

client = signalwire_client(os.getenv("PROJECT_ID"), os.getenv("AUTH_TOKEN"),
                           signalwire_space_url=os.getenv("SPACE_URL"))

# lists messages with optional added filters to narrow results
messages = client.messages.list(date_sent_after=datetime(2022, 0o1, 0o1))

# Sets up an empty array to store messages
d = []

# Appends all matching data from messages into an array
for record in messages:
    if record.direction == "outbound-api":
        d.append((record.sid, record.date_sent, record.price, record.num_segments))

# Puts message log array into dataframe with headers for easier reading.
df = pd.DataFrame(d, columns=('Message SID', 'Date Sent', 'Price', 'Num Segments'))

# Exports dataframe to csv, index=False turns off the indexing for each row
df.to_csv('Messages.csv', index=False, encoding='utf-8')

totalMess = len(df)
totalCost = df['Price'].sum()
formattedCost = "${:,.2f}".format(totalCost)
totalSegments = df['Num Segments'].sum()

# print some quick summaries
print(f"You sent {totalMess} total messages during your selected date range.")
print(f"You sent {totalSegments} total segments during your selected date range.")
print(f"The total cost of messages in your selected date range is approximately {formattedCost} USD.")
