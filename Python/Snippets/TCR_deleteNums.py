import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

# assign client variables
csv_of_nums_to_delete= pd.read_csv("FileName.csv", encoding='utf-8',delimiter=",")
SpaceURL = ''
projectID = ""
authToken = ""
campaignID = ""
host = f"https://{SpaceURL}"


csv_of_nums_to_delete = csv_of_nums_to_delete['Phone Number']
print(csv_of_nums_to_delete)


# Add a + to each element in the list
def prepend(list, str):
    # Using format()
    str += '{0}'
    list = [str.format(i) for i in list]
    return (list)


# Driver function
list = csv_of_nums_to_delete
str = '+'
csv_of_nums_to_delete= (prepend(list, str))


# define URL for API Endpoint
url = f"https://{SpaceURL}/api/relay/rest/registry/beta/campaigns/{campaignID}/numbers?page_size=1000"
payload = {}
headers = {}
response = requests.request("GET", url, headers=headers, data=payload, auth=HTTPBasicAuth(projectID, authToken)).json()
campaignNumbers = response['data']

while "next" in response['links'].keys():
    response = requests.get(host + response['links']['next'], auth=HTTPBasicAuth(projectID, authToken)).json()
    campaignNumbers.extend(response['data'])

print(campaignNumbers)
print(f"There are {len(campaignNumbers)} total numbers in campaign {campaignID}.")

# Sets up an empty array
d = []

# loop through numbers
for number in campaignNumbers:
    phone_number=number['phone_number']['number']
    print(phone_number)
    if phone_number in csv_of_nums_to_delete:
        print('This number is in' + phone_number)
        d.append((number['phone_number']['number'], number['id']))


df = pd.DataFrame(d, columns=(['Phone Number', 'ID']))
print(df.to_string())

list_of_numberID_to_delete = df['ID']
print(list_of_numberID_to_delete)

for n in list_of_numberID_to_delete:
    print('starting to delete')
    delete_number_assignment_url = "https://" + SpaceURL + '/api/relay/rest/registry/beta/numbers/' + n
    headers = {}
    # Make the complete API request for deleting a number assignment
    delete_number_assignment_Request = requests.request("DELETE", delete_number_assignment_url, headers=headers, auth=HTTPBasicAuth(projectID, authToken))
    print("number deleted with assignment id     " + n)

print('These were the numbers and Ids deleted')
print(df)