from signalwire.rest import Client as signalwire_client
import pandas as pd

client = signalwire_client("", "", signalwire_space_url = 'example.signalwire.com')

# Lists all numbers on account
incoming_phone_numbers = client.incoming_phone_numbers.list()

# Sets up an empty array
d = []

# Appends incoming phone numbers into
for record in incoming_phone_numbers:
    d.append((record.phone_number, record.sid))

print(d)

# Puts message log array into dataframe with headers for easier reading.
df = pd.DataFrame(d, columns=('Phone Number', 'PhoneNumberSID'))

print('dataframe')
print('\n')
print(df)

# Exports dataframe to csv, index=False turns off the indexing for each row
df.to_csv('Numbers.csv', index=False, encoding='utf-8')