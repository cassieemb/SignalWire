# Overview 
XML bins, sometimes referred to as LaML bins, create a URL endpoint that responds with a set of instructions that can be executed to handle calls, SMS, or fax.

This application loads XML bins for some of the most common use cases directly into your project.
- Call Forwarding 
- Voicemail Prompt
- Hangup
- Call Forwarding With Record
- Gather Input
- Dial Conference
- Enqueue Caller
- Dial Queue
- Say Message before Bridging Caller and Agent
- Message Forwarding

# What do I need to run this code?

This application doesn't require much - you will need [Python](https://www.python.org/), the [Flask framework](https://www.tutorialspoint.com/python_web_development_libraries/python_web_development_libraries_flask_framework.htm), and a [ngrok tunnel](https://developer.signalwire.com/apis/docs/how-to-test-webhooks-with-ngrok) to reach your localhost or server to host it on. 

# How to Run Application 

To run the application, execute `export FLASK_APP=main.py` then run `flask run`.

You may need to use an SSH tunnel for testing this code – we recommend [ngrok](https://ngrok.com/). After starting the tunnel, you can use the URL you receive from `ngrok` in your webhook configuration for your phone number.


# Sign Up Here

If you would like to test this example out, you can create a SignalWire account and space [here](https://m.signalwire.com/signups/new?s=1).

Please feel free to reach out to us on our [Community Slack](https://signalwire.community/) or create a Support ticket if you need guidance!