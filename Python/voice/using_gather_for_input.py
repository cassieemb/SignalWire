from flask import Flask, request
from signalwire.voice_response import VoiceResponse, Dial, Gather

app = Flask(__name__)


@app.route("/default", methods=['GET', 'POST'])
def acceptCall():
    response = VoiceResponse()

    if 'Digits' in request.values:
        selection = request.values['Digits']

        if selection == '1':
            response.redirect('/recordMessage')
            return str(response)
        elif selection == '2':
            response.redirect('/forwardCall')
            return str(response)
        else:
            response.say("Please select 1 or 2 so that we can direct your call!")

    response.say("Hello! Thank you for calling SignalWire.")

    gather = Gather(num_digits=1)
    gather.say("If you would like to leave a message for our team, please press 1. "
               "If you would like to speak to a team member, please press 2.")

    response.append(gather)
    response.redirect('/default')
    return str(response)


@app.route("/recordMessage", methods=['GET', 'POST'])
def recordVoicemail():
    response = VoiceResponse()
    response.say(
        "Please leave your name and number along with how we can help after the beep, and we will get back to you as "
        "soon "
        "as we can. When you are finished recording, hang up, or press the pound key.")
    response.record(max_length=15, finish_on_key='#', transcribe=True, action="/hangupCall")
    return str(response)


@app.route("/hangupCall", methods=['GET', 'POST'])
def hangupCall():
    response = VoiceResponse()
    response.say("Thank you for your message. Goodbye!")
    response.hangup()
    return str(response)


@app.route("/forwardCall", methods=['GET', 'POST'])
def forwardCall():
    response = VoiceResponse()
    dial = Dial(record='record-from-ringing', recording_status_callback='https://example.com/recording_status')
    dial.number('+12141111111')
    response.append(dial)
    return str(response)


if __name__ == "__main__":
    app.run(debug=True)
