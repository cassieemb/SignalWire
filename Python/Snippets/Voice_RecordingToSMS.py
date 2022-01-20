from flask import Flask, request
from signalwire.rest import Client as signalwire_client

app = Flask(__name__)


@app.route("/message", methods=["POST"])
def message():
    # accept incoming parameters and store them. Feel free to add any extra parameters that you would like to print to
    # to console or add to your message. This example will show CallSID, and recording URL.
    call_sid = request.form.get('CallSid')
    recording_url = request.form.get('RecordingUrl')

    # create a client object connected to our account & project
    client = signalwire_client("ProjectID", "AuthToken", signalwire_space_url = 'spaceURL.signalwire.com')

    # create a text message and send ourselves the text
    m = client.messages.create(
        body='You have received a voicemail! The recording URL is as follows: "' + recording_url +
             '" and the Call SID is ' + call_sid,
        from_='+12085812340',
        to='+12147903161'
    )
    return recording_url


if __name__ == "__main__":
    app.run()