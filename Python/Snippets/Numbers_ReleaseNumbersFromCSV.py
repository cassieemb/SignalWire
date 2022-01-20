from signalwire.rest import Client as signalwire_client
import csv

client = signalwire_client("ProjectID", "AuthToken",
signalwire_space_url='example.signalwire.com')

incoming_phone_numbers = client.incoming_phone_numbers.list()
print("Total Numbers -- " + str(len(incoming_phone_numbers)))

results = []

with open("Numbers.csv", 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        if "+" not in row[0]:
            results.append("+" + row[0])
        else:
            results.append(row[0])
print(results)

for record in incoming_phone_numbers:
    if record.phone_number in results:
        print("deleting number -- " + record.phone_number)
        client.incoming_phone_numbers(record.sid).delete()