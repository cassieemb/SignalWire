from flask import Flask, request
import numpy as np
import pandas as pd
from signalwire.rest import Client as signalwire_client
import atexit

app = Flask(__name__)

client = signalwire_client("ProjectID", "AuthToken",
                           signalwire_space_url='example.signalwire.com')
callArray = []

def onExitApp(dataframe):
    dataframe.to_csv('Calls.csv', index=False, encoding='utf-8')
    print("Inbound callback app exited, goodbye!")

df = pd.DataFrame()
atexit.register(onExitApp, dataframe = df)

@app.route("/incomingCalls", methods=['POST'])
def incoming_calls():
    # store incoming request parameters in variables
    call_sid = request.values.get('CallSid')
    call_status = request.values.get('CallStatus')
    event_timestamp = request.values.get('Timestamp')
    to_number = request.values.get('To', None)
    from_number = request.values.get('From', None)
    call_duration = request.values.get('CallDuration', None)
    audio_in_mos = request.values.get('AudioInMos', None)

   # append call data to array
    callArray.append([call_sid, call_status, event_timestamp, to_number, from_number, call_duration, audio_in_mos])

    # create dataframe with headers from call array
    df = pd.DataFrame(callArray, columns=('Call SID', 'Call Status', 'Event Timestamp', 'To Number', 'From Number', 'Call Duration(s)', 'Audio in MOS'))

    # convert all None values to NaN so it can be used in calculations
    # convert duration and audio mos score from strings to int & float
    df = df.fillna(value=np.nan)
    df['Call Duration(s)'] = df['Call Duration(s)'].astype(float)
    df['Audio in MOS'] = df['Audio in MOS'].astype(float)

    totalCalls = len(callArray)
    totalCallDuration = df['Call Duration(s)'].sum(skipna=True)
    totalCallDurationinMinutes = float(totalCallDuration / 60)
    roundedMinutes = round(totalCallDurationinMinutes, 2)
    avgAudioMOS = df['Audio in MOS'].mean(skipna=True)

    print("Current Inbound Call Stats: ")
    print('----------------------------')
    print('Total # of Calls: ' + str(totalCalls))
    print("Call Duration in Minutes: " + str(roundedMinutes))
    print('Average Audio Quality (measured in MOS): ' + str(avgAudioMOS))
    print(df.to_string())

    return ('', 200)

if __name__ == "__main__":
    app.run()