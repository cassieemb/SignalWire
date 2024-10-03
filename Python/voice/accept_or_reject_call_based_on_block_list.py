from flask import Flask, request
from signalwire.voice_response import VoiceResponse
import os
from dotenv import load_dotenv

load_dotenv('../../.env')

app = Flask(__name__)


def get_blocklist():
    return os.getenv('BLOCK_LIST').split(',')


@app.route('/check', methods=['POST'])
def check_number():
    response = VoiceResponse()
    from_number = request.form.get('From')
    print(from_number)

    if from_number not in get_blocklist():
        response.redirect(os.environ.get('REDIRECT_PATH'))
    else:
        response.hangup()

    return response.to_xml()


if __name__ == "__main__":
    app.run()
