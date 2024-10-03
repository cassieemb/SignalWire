from flask import Flask, request
import logging
import pandas as pd
from signalwire.rest import Client as signalwire_client
import atexit
import os
from dotenv import load_dotenv

load_dotenv('../../.env')
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# create an empty array to keep track of all of our undelivered or failed messages during the time this app is run
undeliveredArray = []


# define actions to take when flask app is closed
# export dataframe of all failed or undelivered messages to CSV with added detail
def onExitApp(dataframe):
    dataframe.to_csv('failedAndUndeliveredMessages.csv', index=False, encoding='utf-8')
    print('SMS Callback App Exited')


# authenticate the SignalWire client
client = signalwire_client(os.getenv("PROJECT_ID"), os.getenv("AUTH_TOKEN"),
                           signalwire_space_url=os.getenv("SPACE_URL"))


# define route for SMS status callbacks to be posted to
@app.route("/smsErrorTracker", methods=['POST'])
def newest_message():
    # get message sid, message status, and error code (if it exists) from callback parameters
    # if they don't exist, set to None
    message_sid = request.values.get('MessageSid', None)
    message_status = request.values.get('MessageStatus', None)
    error_code = request.values.get('ErrorCode', None)

    # log every message that comes in to console
    logging.info('SID: {}, Status: {}, ErrorCode: {}'.format(message_sid, message_status, error_code))

    # if the message is undelivered or failed, use message SID to fetch additional data
    # about the failed message
    if message_status == "undelivered" or message_status == "failed":
        message = client.messages(message_sid).fetch()

        # add identifying data from newest message to undelivered array
        undeliveredArray.append(
            [message_sid, message_status, error_code, message.error_message, message.date_sent, message.to,
             message.from_, message.body])
        # insert array into dataframe with columns for easier reading
        df = pd.DataFrame(undeliveredArray, columns=(
            'Message Sid', 'Message Status', 'Error Code', 'Error Message', 'Date Sent', 'To', 'From', 'Body'))
        # print dataframe to string for nicer formatting and set dataframe to our parameter in function for handling
        # app exit
        print(df.to_string())
        atexit.register(onExitApp, dataframe=df)

        # return 200OK
    return '', 200


if __name__ == "__main__":
    app.run()
