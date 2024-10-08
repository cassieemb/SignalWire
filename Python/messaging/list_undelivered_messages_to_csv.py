from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv('../../.env')

client = signalwire_client(os.getenv("PROJECT_ID"), os.getenv("AUTH_TOKEN"),
                           signalwire_space_url=os.getenv("SPACE_URL"))

messages = client.messages.list(date_sent_after=datetime(2020, 0o3, 13))

d = []

for record in messages:
    if (record.status == 'failed') or (record.status == 'undelivered') and (
            record.error_message != "Unreachable destination handset"):
        d.append((record.from_, record.to, record.date_sent, record.sid, record.error_code, record.error_message))

df = pd.DataFrame(d, columns=('From', 'To', 'Date', 'MessageSID', 'Error Code', 'Error Message'))
df.to_csv('UndeliveredMessages.csv', index=False, encoding='utf-8')
