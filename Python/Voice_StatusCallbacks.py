from flask import Flask, request
import logging
import pandas as pd
from signalwire.rest import Client as signalwire_client
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# create empty arrays to store our call records - one for failed only and one to handle all other end stage statuses (not queued, not ringing, not answered, etc)
failedCallArray = []
allCallArray = []

# authenticate the SignalWire client
client = signalwire_client(os.getenv("PROJECT_ID"), os.getenv("AUTH_TOKEN"),
                           signalwire_space_url=os.getenv("SPACE_URL"))


@app.route("/CallStatus", methods=['POST'])
def incoming_calls():
    # grab incoming parameters posted to webhook and assign them variables
    call_sid = request.values.get('CallSid', None)
    call_status = request.values.get('CallStatus', None)
    event_timestamp = request.values.get('Timestamp', None)
    recording_url = request.values.get('RecordingUrl', None)
    call_direction = request.values.get('Direction', None)
    to_number = request.values.get('To', None)
    from_number = request.values.get('From', None)

    # log some basic information to print to console for EVERY status change
    logging.info('SID: {}, Status: {}, Timestamp: {}, Direction: {}'.format(call_sid, call_status, event_timestamp, call_direction))

    # create a separate array for all end stage statuse updates and add them to our call log table, display updated table
    if (call_status != 'ringing' and call_status != 'initiated' and call_status != 'answered' and call_status != 'in-progress' and call_status != 'queued' and call_status != 'failed'):
        allCallArray.append([call_sid, call_status, event_timestamp, call_direction, to_number, from_number, recording_url])
        adf = pd.DataFrame(allCallArray, columns=('Call SID', 'Call Status', 'Event Timestamp', 'Call Direction', 'To Number', 'From Number',
        'Recording URL (if present)'))
        print("All Calls")
        print(adf.to_string())

    # if call status is failed, log call record to call failure table and display table
    if (call_status == "failed"):
        failedCallArray.append([call_sid, call_status, event_timestamp, call_direction, to_number, from_number, recording_url])
        df = pd.DataFrame(failedCallArray, columns=('Call SID', 'Call Status', 'Event Timestamp', 'Call Direction', 'To Number', 'From Number', 'Recording URL (if present)'))
        print("Failed Calls")
        print(df.to_string())

        # if the number of failed calls is over 100
        if len(failedCallArray) > 100:
            # download call logs with necessary data to CSV and send an sms alert of the failures
            df.to_csv('failedCallReport.csv', index=False, encoding='utf-8')
            m = client.messages.create(
                body='Call Failure Alert! You have received 100 call failures. '
                     'A CSV of the failures has been downloaded and the failure database will now reset.',
                from_='+12022358941',
                to='+12147903161')
            print("CSV of Failed Calls Downloaded & Message Alert Sent")

            # clear array to start adding fresh logs again
            while len(failedCallArray) > 0:
                failedCallArray.pop()

    # Return 200 OK
    return ('', 200)

if __name__ == "__main__":
    app.run()
