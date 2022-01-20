from flask import Flask, request
from signalwire.rest import Client as signalwire_client

app = Flask(__name__)

# authenticate the SignalWire client
client = signalwire_client("ProjectID",
                           "AuthToken",
                           signalwire_space_url='example.signalwire.com')

@app.route("/MessageStatus", methods=['POST'])
def incoming_sms():
    message_sid = request.values.get('MessageSid', None)
    message_status = request.values.get('MessageStatus', None)

    if (message_status != "sending" and message_status != "sent" and message_status != "queued"):
        # use this to update the message body but keep the message record
        message = client.messages(message_sid) .update(body='')
        print("Message Redacted")

        # uncomment this line and comment the above one if instead you want to FULLY delete the message, erasing all message history
        # client.messages(message_sid).delete()
        # print("Message Deleted")
    return ('', 200)

if __name__ == "__main__":
    app.run()





