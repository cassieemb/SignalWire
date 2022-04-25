import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

# assign auth variables
SpaceURL = 'EXAMPLE.signalwire.com'
projectID = "ProjectID"
authToken = "AuthToken"
host = f"https://{SpaceURL}"

# define URL for API Endpoint
url = f"https://{SpaceURL}/api/video/room_sessions?page_size=1000"
payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload, auth=HTTPBasicAuth(projectID, authToken)).json()
roomSessions = response['data']

while "next" in response['links'].keys():
     response = requests.get(host + response['links']['next'], auth=HTTPBasicAuth(projectID, authToken)).json()
     roomSessions.extend(response['data'])

# Sets up an empty array
d = []

# loop through sessions
for session in roomSessions:
    d.append((session['id'], session['name'], session['start_time'], session['end_time'], session['duration'], session['cost_in_dollars']))

df = pd.DataFrame(d, columns=('Room ID', 'Name', 'Start Time', 'End Time', 'Duration (seconds)', 'Cost in Dollars'))
print(df.to_string())

print(f"There were {len(df)} total room sessions with a total duration of {round((df['Duration (seconds)'].sum())/60, 2)} minutes and a total cost of {'${:,.2f}'.format(df['Cost in Dollars'].sum())} dollars.")

df.to_csv('RoomSessionData.csv', index=False, encoding='utf-8')