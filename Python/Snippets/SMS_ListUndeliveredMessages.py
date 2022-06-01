from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd

client = signalwire_client("", "",
                           signalwire_space_url='.signalwire.com')

messages = client.messages.list(date_sent_after=datetime(2022, 0o3, 13))

d = []

for record in messages:
    if (record.status == 'failed') or (record.status == 'undelivered') and (record.error_message != "Unreachable destination handset"):
        d.append((record.from_, record.to, record.date_sent, record.sid, record.error_code, record.error_message))


df = pd.DataFrame(d, columns=('From', 'To', 'Date', 'MessageSID', 'Error Code', 'Error Message'))
df.to_csv('UndeliveredMessages.csv', index=False, encoding='utf-8')