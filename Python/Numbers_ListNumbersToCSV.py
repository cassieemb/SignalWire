from signalwire.rest import Client as signalwire_client
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

client = signalwire_client(os.getenv("PROJECT_ID"), os.getenv("AUTH_TOKEN"), signalwire_space_url=os.getenv("SPACE_URL"))

# Lists all numbers on account
incoming_phone_numbers = client.incoming_phone_numbers.list()

# Sets up an empty array
d = []

# Appends incoming phone numbers into
for record in incoming_phone_numbers:
    d.append(record.phone_number)

# Puts message log array into dataframe with headers for easier reading.
df = pd.DataFrame(d, columns=['Phone Number'])

# Exports dataframe to csv, index=False turns off the indexing for each row
df.to_csv('Numbers.csv', index=False, encoding='utf-8')
