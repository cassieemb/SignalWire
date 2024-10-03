from signalwire.rest import Client as signalwire_client
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv('../../.env')

client = signalwire_client(os.getenv("PROJECT_ID"), os.getenv("AUTH_TOKEN"),
                           signalwire_space_url=os.getenv("SPACE_URL"))

messages = client.messages.list(date_sent_after=datetime(2022, 0o3, 30))

m = []

for record in messages:
    m.append(record.status)

# Transfer Variables to Int
num_sent = int(m.count("sent"))
num_received = int(m.count("received"))
num_delivered = int(m.count("delivered"))
num_undelivered = int(m.count("undelivered"))

# Calculate Total Number Outbound Messages
num_outbound_messages = num_sent + num_delivered + num_undelivered
num_inbound_messages = num_received

# Make it look Pretty
print(f"You Have {str(num_sent)} Sent Messages")
print(f"You Have {str(num_delivered)} Delivered Messages")
print(f"You Have {str(num_undelivered)} Undelivered Messages")
print(f"You Also Have {str(num_received)} Received Messages")
