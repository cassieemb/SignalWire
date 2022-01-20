from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd

client = signalwire_client("ProjectID", "AuthToken",
                           signalwire_space_url='YOURSPACE.signalwire.com')

messages = client.messages.list(date_sent_after=datetime(2021, 10, 20),
                                date_sent_before=datetime(2021, 10, 30),
                                from_="+1xxxxxxxxxx",
                                )

d = []

for record in messages:
    if record.status == "undelivered":
        d.append((record.from_, record.to, record.date_sent, record.sid, record.error_code))


df = pd.DataFrame(d, columns=('From', 'To', 'Date', 'MessageSID', 'Error Code'))

print(df)

df.to_csv('UndeliveredMessages.csv', index=False, encoding='utf-8')