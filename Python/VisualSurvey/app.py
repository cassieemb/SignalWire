from flask import Flask, request, url_for, Response, jsonify
from flask_cors import CORS
from signalwire.voice_response import VoiceResponse, Gather, Say
from signalwire.rest import Client as signalwire_client
from sheets import sheet
from datetime import datetime, timezone
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.app_context().push()

answers = dict()
client = signalwire_client(os.getenv('SIGNALWIRE_PROJECT'), os.getenv('SIGNALWIRE_TOKEN'),
                           signalwire_space_url=os.getenv('SIGNALWIRE_SPACE'))


def toXML(resp):
    resp = Response(str(resp))
    resp.headers['Content-Type'] = 'text/xml'
    return resp


@app.after_request
def after_request(response):
    white_origin = [os.getenv("HOST_NAME"), 'http://localhost:3000']
    if request.headers['Origin'] in white_origin:
        response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
        response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response


@app.route('/entry', methods=['GET', 'POST'])
def description():
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()

    date_time = datetime.datetime.fromtimestamp(utc_timestamp)
    str_date_time = date_time.strftime("%m-%d-%Y, %H:%M:%S")

    answers[request.values.get('CallSid')] = []
    answers[request.values.get('CallSid')].append(request.values.get('CallSid'))
    answers[request.values.get('CallSid')].append(request.values.get('To'))
    answers[request.values.get('CallSid')].append(request.values.get('From'))
    answers[request.values.get('CallSid')].append(str_date_time)

    response = VoiceResponse()
    with response.gather(num_digits=1, action=url_for('question_zero'), method='POST') as g:
        g.say("Thanks for calling the FedUPS Lost Package Center. In order to locate your package, please answer a "
              "series of questions to gather the necessary information. If you would like to answer these "
              "questions using audio and touch tones only, press 1. If you would like to receive an "
              "SMS containing a link to answer these questions via your web browser, press 2.")
        response.append(g)
        return toXML(response)


@app.route('/question_zero', methods=['GET', 'POST'])
def question_zero():
    digits = int(request.values.get('Digits'))
    response = VoiceResponse()

    if digits == 1:
        with response.gather(num_digits=1, action=url_for('question_one'), method='POST') as g:
            g.say("You have selected audio & touch tones only. Press any key to begin answering questions.")
            response.append(g)
    elif digits == 2:
        with response.gather(num_digits=10, action=url_for('send_link'), method='POST') as g:
            g.say("You have selected to receive a link via SMS. Please enter the 10 digit phone number and ensure that "
                  "it is a SMS capable US or Canadian phone number.")
            response.append(g)
    else:
        response.say("Sorry, that is not acceptable input.")
        response.redirect('/entry')

    return toXML(response)


@app.route('/send_link', methods=['GET', 'POST'])
def send_link():
    digits = request.values.get('Digits')
    callSID = request.values.get('CallSid')
    host_link = os.getenv("HOST_NAME") + '/'
    custom_link = host_link + callSID

    # add link to web form on react app
    message = client.messages.create(
        from_=os.environ['SIGNALWIRE_FROM_NUMBER'],
        body='FedUPS: Please click the following link to help us locate your missing package. ' + custom_link,
        to="+1" + digits
    )
    print(message.sid)
    response = VoiceResponse()
    response.say(
        "Thank you for calling. An SMS has been sent and you may now complete the questionnaire at your convenience "
        "via web browser. "
        "Goodbye!")
    response.hangup()
    return toXML(response)


@app.route('/process_web_form', methods=['POST'])
def read_results():
    # get values from UI
    data = request.get_json()
    print(data)

    callSIDDict = data.get('callSID')
    callSID = callSIDDict.get('callSID')
    trackingNumber = data.get('trackingNumber', ' ')
    typeOfResidence = data.get('typeResidence', ' ')
    arrivalDate = data.get('arrivalDate', ' ')
    callbackNumber = data.get('callbackNumber', ' ')
    firstName = data.get('firstName', ' ')
    lastName = data.get('lastName', ' ')

    # fetch call data using fetch call API and call SID
    call = client.calls(callSID).fetch()
    toNumber = call.to_formatted
    fromNumber = call.from_formatted
    timestamp = str(call.start_time)

    # create record and append to array
    answers[callSID] = []
    answers[callSID].append(callSID)
    answers[callSID].append(toNumber)
    answers[callSID].append(fromNumber)
    answers[callSID].append(timestamp)
    answers[callSID].append(trackingNumber)
    answers[callSID].append(arrivalDate)
    answers[callSID].append(typeOfResidence)
    answers[callSID].append(callbackNumber)
    answers[callSID].append(firstName)
    answers[callSID].append(lastName)
    answers[callSID].append('Completed by Browser')

    print(answers[callSID])

    # add to google sheet
    sheet.insert_row(answers[callSID], 2)
    answers.pop(callSID)
    print("Sheet updated")

    return callSID


@app.route('/question_one', methods=['GET', 'POST'])
def question_one():
    response = VoiceResponse()
    with response.gather(num_digits=10, action=url_for('question_two'), method="POST") as g:
        g.say('Please enter your 10 digit tracking number.')
        response.append(g)
        return toXML(response)


@app.route('/question_two', methods=['GET', 'POST'])
def question_two():
    digits = request.values.get('Digits')
    answers[request.values.get('CallSid')].append(digits)

    response = VoiceResponse()
    with response.gather(num_digits=8, action=url_for('question_three'), method="POST") as g:
        g.say(
            'Thank you. What was your expected arrival date? Please enter the date in the order of year, month, '
            'and day '
            'leaving out any spaces or dashes. For example, July 1st 2020 would be 2 0 2 0 0 7 0 1.')
        response.append(g)
        return toXML(response)


@app.route('/question_three', methods=['GET', 'POST'])
def question_three():
    # turn digits into string so we can splice it to add date formatting
    digits = str(request.values.get('Digits'))
    date = digits[0:4] + "/" + digits[4:6] + "/" + digits[6:]
    answers[request.values.get('CallSid')].append(date)

    response = VoiceResponse()
    with response.gather(num_digits=1, action=url_for('question_four'), method="POST") as g:
        g.say('Is this package supposed to be delivered to a house, apartment, or office building? Press 1 for house, '
              '2 for apartment, or 3 for office. ')
        response.append(g)
        return toXML(response)


@app.route('/question_four', methods=['GET', 'POST'])
def question_four():
    digit = request.values.get('Digits')
    if digit == '1':
        answers[request.values.get('CallSid')].append('House')
    elif digit == '2':
        answers[request.values.get('CallSid')].append('Apartment')
    elif digit == '3':
        answers[request.values.get('CallSid')].append('Office')
    else:
        answers[request.values.get('CallSid')].append('Unclear.')

    response = VoiceResponse()

    with response.gather(num_digits=10, action=url_for('question_five'), method="POST") as g:
        g.say('What is your preferred callback phone number?')
        response.append(g)
        return toXML(response)


@app.route('/question_five', methods=['GET', 'POST'])
def question_five():
    digits = request.values.get('Digits')
    answers[request.values.get('CallSid')].append(digits)

    response = VoiceResponse()
    with response.gather(input="speech", action=url_for('question_six'), method="POST") as g:
        g.say('What is your first name?')
        response.append(g)
        return toXML(response)


@app.route('/question_six', methods=['GET', 'POST'])
def question_six():
    speechResult = request.values.get('SpeechResult')
    answers[request.values.get('CallSid')].append(speechResult)

    response = VoiceResponse()
    with response.gather(input="speech", action=url_for('end_questionnaire'), method="POST") as g:
        g.say('What is your last name?')
        response.append(g)
        return toXML(response)


@app.route('/end_questionnaire', methods=['GET', 'POST'])
def end_questionnaire():
    speechResult = request.values.get('SpeechResult')
    answers[request.values.get('CallSid')].append(speechResult)
    answers[request.values.get('CallSid')].append('Completed By Phone')

    # add to google sheet
    sheet.insert_row(answers[request.values.get('CallSid')], 2)
    answers.pop(request.values.get('CallSid'))

    response = VoiceResponse()
    response.say(
        'Thank you for answering these questions. Your responses will be sent to our office. Have a great day!')

    return toXML(response)


if __name__ == "__main__":
    app.run()
