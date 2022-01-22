import pandas as pd
from signalwire.rest import Client as signalwire_client
import csv

# import client
client = signalwire_client("ProjectID", "AuthToken", signalwire_space_url = 'example.signalwire.com')

# define results dict for storing client records from csv and messages list for storing data about send
results = {}
messages = []

# read in CSV to dict where phone number is the key and [first name, last name] is the value
with open("src/bulk_sms.csv", 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        results[row['Number']] = [row['First'], row['Last']]
print(results)

# link placeholder if links need to be sent with the message
# use results[customer] to query database by phone number if customized URLs are needed
smsLink = "https://developer.signalwire.com/"

# loop through entries and grab first name
for customer in results:
    # store name for matched phone number in variable to use in template
    firstName = (results[str(customer)][0])
    print(f"messaging {firstName}")

    # set formatted number to the E164 version using ternary operator
    formattedNumber = "+" + customer if "+" not in customer else customer

    # send message
    message = client.messages.create(
        from_='+1xxxxxxxxxx',
        body=f"Hello {firstName}, you can access our developer portal at {smsLink} ",
        to=formattedNumber)

    messages.append((message.sid, message.from_, message.to, message.body, message.date_sent))

# Puts call log array into dataframe with headers for easier reading.
df = pd.DataFrame(messages, columns=('Sid', 'From', 'To', 'Body', 'Date/Time Sent'))

print(df.to_string)

df.to_csv('BulkSendDetails.csv', index=False, encoding='utf-8')