from flask import Flask, request
from signalwire.voice_response import VoiceResponse, Dial

app = Flask(__name__)

# create moderator team array and add numbers of all moderators
# make sure that both phone numbers are in E164+ format
moderator_team = ['+12148888888', '+13468888888']


@app.route("/default", methods=['GET', 'POST'])
def call():
    # instantiate voice response
    response = VoiceResponse()

    # use with statement to manage dial resource and use if/else
    with Dial() as dial:
        # check moderator team array for from number to see if caller is moderator
        # if caller is moderator, begin recording call and set call to start on enter and end on exit
        if request.values.get('From') in moderator_team:
            dial.conference(
                'A1 Room',
                record='record-from-start',
                start_conference_on_enter=True,
                end_conference_on_exit=True)
        else:
            # if caller is not moderator, advise them to wait and put them in conference as regular participant
            dial.conference('A1 Room', start_conference_on_enter=False)
            response.say('Thank you for joining A1 Room. This conference will start when your moderator enters the room.')

    # append dial action to response
    response.append(dial)

    # convert response to string
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)