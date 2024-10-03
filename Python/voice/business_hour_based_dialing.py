from flask import Flask
from signalwire.voice_response import VoiceResponse, Dial
from datetime import datetime
from pytz import timezone

app = Flask(__name__)


# check current time in EST and see if it's between business hours 9am-8pm
# Send to open route if between business hours, closed route when not in business hours
@app.route('/checkTime', methods=['GET', 'POST'])
def checkTime():
    response = VoiceResponse()
    tz = timezone('US/Eastern')
    timeNow = datetime.now(tz)

    # The year, month, and date don't matter here - we will only be comparing the time component
    opening = datetime(2010, 1, 1, 9, 0, 0)  # 9AM
    closing = datetime(2010, 1, 1, 20, 0, 0)  # 8PM

    # check if between hours of 9AM-8PM
    if opening.time() < timeNow.time() < closing.time():
        # check if M-F
        if timeNow.isoweekday() in range(1, 6):
            response.redirect(url='/open')
            print('Time Now is: ' + str(timeNow.time()))
            print("That means we're open!")
    else:
        response.redirect(url='/closed')
        print('Time Now is: ' + str(timeNow.time()))
        print("That means we're closed!")

    return response.to_xml()


# Route if calls are within business hours
@app.route('/open', methods=['GET', 'POST'])
def inBusinessHours():
    response = VoiceResponse()
    dial = Dial(record='true')
    dial.number('+12342556182')
    response.append(dial)
    return response.to_xml()


# Route to voicemail if calls are outside of business hours
@app.route('/closed', methods=['GET', 'POST'])
def offBusinessHours():
    response = VoiceResponse()
    response.say("Thank you for calling! Our business hours are 9AM-8PM Eastern Time, Monday through Friday. "
                 "Please record a message with your name and number and we will get back to you!")
    response.record(action='/hangup', method='POST', max_length=15, finish_on_key='#')
    return response.to_xml()


# hangup bin used for action url in above route
@app.route('/hangup', methods=['POST'])
def hangup():
    response = VoiceResponse()
    response.say("Thank you for your message. Goodbye!")
    response.hangup()
    return str(response)


if __name__ == "__main__":
    app.run()
