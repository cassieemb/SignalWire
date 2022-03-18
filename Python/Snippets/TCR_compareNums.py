from signalwire.rest import Client as signalwire_client
import csv

# define your variables here so they don't need to be hardcoded
SpaceURL = ''
projectID = ""
authToken = ""
PathToCSV = 'FileName.csv'

# Replace project ID, auth token, and space URL
client = signalwire_client(projectID, authToken, signalwire_space_url=SpaceURL)

# List and print all numbers on account
incoming_phone_numbers = client.incoming_phone_numbers.list()
print("Total Numbers -- " + str(len(incoming_phone_numbers)))

# create empty array to store numbers that are already registered
results = []
unregistered = []

# Open CSV file with registered numbers
with open(PathToCSV, 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    # Change to E164 format if it's not already in that format
    for row in reader:
        if "+" not in row[0]:
            results.append("+" + row[0])
        else:
            results.append(row[0])


# Loop through all account numbers, add number to list if unregistered
for record in incoming_phone_numbers:
    if record.phone_number in results:
        continue
    else:
        print('unregistered number --' + record.phone_number)
        unregistered.append(record.phone_number)

print(unregistered)
