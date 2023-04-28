from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

client = signalwire_client(os.getenv("PROJECT_ID"), os.getenv("AUTH_TOKEN"),
                           signalwire_space_url=os.getenv("SPACE_URL"))

calls = client.calls.list(start_time_after=datetime(2022, 4, 1), start_time_before=datetime(2022, 4, 30))

d = []
direction = []

for record in calls:
    d.append((record.from_, record.to, record.start_time, record.sid, record.price, record.direction, record.duration))
    direction.append(record.direction)

total_inbound=int(direction.count("inbound"))
total_outbound=int(direction.count("outbound"))

df = pd.DataFrame(d, columns=('From', 'To', 'Date', 'Call SID',  'Price', 'Call Direction', 'Call Duration (s)'))
print(df)
df.to_csv('MarchCalls.csv', index=False, encoding='utf-8')

totalCalls = len(df)
totalCost = df['Price'].sum()
formattedCost = "${:,.2f}".format(totalCost)
totalDuration = round((df['Call Duration (s)'].sum())/60, 2)

print("You had " + str(totalCalls) + " total calls during your selected date range.")
print("There were " + str(total_inbound) + " inbound calls and " + str(total_outbound) + " outbound calls.")
print("The total cost of calls in your selected date range is approximately " + formattedCost + " USD.")
print("there was a total duration of " + str(totalDuration) + " minutes.")
