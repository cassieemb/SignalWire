from signalwire.rest import Client as signalwire_client
from datetime import datetime

client = signalwire_client("ProjectID",
                           "AuthToken",
                           signalwire_space_url='example.signalwire.com')

messages = client.messages.list(date_sent=datetime(2021, 5, 25, 0, 0, 0))

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
print("You Have " + str(num_sent) + " Sent Messages")
print("You Have " + str(num_delivered) + " Delivered Messages")
print("You Have " + str(num_undelivered) + " Undelivered Messages")
print("\nYou Also Have " + str(num_received) + " Received Messages")
