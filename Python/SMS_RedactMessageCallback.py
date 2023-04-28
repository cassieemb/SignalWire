from flask import Flask, request
from signalwire.rest import Client as signalwire_client
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

client = signalwire_client(os.getenv("PROJECT_ID"), os.getenv("AUTH_TOKEN"),
                           signalwire_space_url=os.getenv("SPACE_URL"))


@app.route("/MessageStatus", methods=['POST'])
def incoming_sms():
    message_sid = request.values.get('MessageSid', None)
    message_status = request.values.get('MessageStatus', None)

    if message_status not in ["sending", "queued"]:
        # use the following code to redact the body but keep the message record
        client.messages(message_sid).update(body='')
        print("Message Redacted")

        # use the following code to delete the whole message record
        # client.messages(message_sid).delete()
        # print("Message Deleted")
    return '', 200


if __name__ == "__main__":
    app.run()
