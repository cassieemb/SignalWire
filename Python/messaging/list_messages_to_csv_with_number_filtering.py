from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv('../../.env')

client = signalwire_client(os.getenv("PROJECT_ID"), os.getenv("AUTH_TOKEN"),
                           signalwire_space_url=os.getenv("SPACE_URL"))

from_numbers = ["+12223334444", "+15556667777"]
d = []

for number in from_numbers:
    messages = client.messages.list(from_=number, date_sent_after=(datetime(2021, 11, 30)))
    for record in messages:
        d.append(
            (record.from_, record.to, record.date_sent, record.status, record.sid, record.body, record.error_message))

df = pd.DataFrame(d, columns=('From', 'To', 'Date', 'Status', 'MessageSID', 'Message Body', 'Error Message'))

df.to_csv('SelectedMessages.csv', index=False, encoding='utf-8')
