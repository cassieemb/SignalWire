from flask import Flask, request
import logging
import pandas as pd
from signalwire.rest import Client as signalwire_client
import atexit

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

undeliveredArray = []

def onExitApp(dataframe):
    dataframe.to_csv('failedAndUndeliveredMessages.csv', index=False, encoding='utf-8')
    print('SMS Callback App Exited')

# authenticate the SignalWire client
client = signalwire_client("ProjectID",
                           "AuthToken",
                           signalwire_space_url='SpaceURL.signalwire.com')

@app.route("/MessageStatus", methods=['POST'])
def incoming_sms():
    message_sid = request.values.get('MessageSid', None)
    message_status = request.values.get('MessageStatus', None)
    error_code = request.values.get('ErrorCode', None)
    logging.info('SID: {}, Status: {}, ErrorCode: {}'.format(message_sid, message_status, error_code))

    if (message_status == "undelivered" or message_status == "failed"):
        message = client.messages(message_sid).fetch()
        undeliveredArray.append([message_sid, message_status, error_code, message.error_message, message.date_sent, message.to, message.from_, message.body])
        df = pd.DataFrame(undeliveredArray, columns=('Message Sid', 'Message Status', 'Error Code', 'Error Message', 'Date Sent', 'To', 'From', 'Body'))
        print(df.to_string())
        atexit.register(onExitApp, dataframe=df)

    return ('', 200)

if __name__ == "__main__":
    app.run()