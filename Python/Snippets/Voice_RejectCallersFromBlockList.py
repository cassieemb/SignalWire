from flask import Flask, request
from signalwire.voice_response import VoiceResponse
import os

app = Flask(__name__)


def get_blocklist():
    # there is a default here you can change if you don't want to use the environment variable
    return os.getenv('BLOCK_LIST', '+1555778899').split(',')


@app.route('/check', methods=['POST'])
def check_number():
    response = VoiceResponse()
    from_number = request.form.get('From')
    print(from_number)

    if from_number not in get_blocklist():
        response.redirect(os.environ.get('REDIRECT_PATH', 'https://some_redirect_url'))
    else:
        response.hangup()

    return response.to_xml()


if __name__ == "__main__":
    app.run()
