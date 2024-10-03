from flask import Flask, request
from signalwire.rest import Client as signalwire_client
import os
from dotenv import load_dotenv

load_dotenv('../../.env')
app = Flask(__name__)


@app.route("/message", methods=["POST"])
def message():
    # accept incoming parameters and store them. Feel free to add any extra parameters that you would like to print to
    # to console or add to your message. This example will show CallSID, from number, and transcription text.
    call_sid = request.form.get('CallSid')
    transcription_text = request.form.get('TranscriptionText')
    from_number = request.form.get('From')

    # create a client object connected to our account & project
    client = signalwire_client(os.getenv("PROJECT_ID"), os.getenv("AUTH_TOKEN"), signalwire_space_url=os.getenv("SPACE_URL"))

    # create a text message and send ourselves the text
    m = client.messages.create(
        body='You have received a voicemail from the number ' + from_number +
             '. The voicemail transcription is as follows: "' + transcription_text +
             '" and the Call SID is ' + call_sid,
        from_=os.getenv("FROM_NUMBER"),
        to=os.getenv("PERSONAL_NUMBER")
    )
    return transcription_text


if __name__ == "__main__":
    app.run()
