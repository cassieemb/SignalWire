from flask import Flask, request
from signalwire.voice_response import VoiceResponse, Dial, Gather
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

support_agents = ['+14803769009']

@app.route("/voice", methods=["GET", "POST"])
def voice():
    response = VoiceResponse()

    if "Digits" in request.values:
        selection = request.values['Digits']

        if request.values.get('From') in support_agents:
            if selection == "1":
                response.say("You will now be connected to the customer, please hold. "
                             "The next voice you hear will be the customer's.")
                dial = Dial()
                dial.queue("support")
                response.append(dial)

            elif selection == "2":
                response.say("That's okay, everyone needs a break! See you later for more customer calls, goodbye!")
                response.hangup()

            else:
                response.say("Please select 1 or 2 so that we can direct your call!")
    else:
        if request.values.get('From') in support_agents:
            gather = Gather(num_digits=1)
            gather.say(
                "Hello team member. Thank you for dialing in. Press 1 to connect to the next caller or "
                "press 2 to end the call if you are not ready to speak to customers.")
            response.append(gather)

        else:
            response.say("Hello and thank you for calling! All of our agents are currently on the line with other "
                         "customers. Please hold, and someone will be with you soon.")
            response.enqueue("support")

    response.redirect("/voice")

    return str(response)

if __name__ == "__main__":
    app.run()
