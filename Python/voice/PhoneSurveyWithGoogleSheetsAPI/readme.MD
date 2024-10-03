# Use Google Sheets and Python to Create an Outbound/Inbound Phone Survey

This code will show you how you can use the google sheets API as a database alternative to store the results of a phone
survey. This survey can be attached as a webhook to a phone number for inbound calls or sent outbound as the URL for
outbound calls.

In this case, we will show how it could be used to create a COVID19 health survey that will gather and append the call
SID, from number, to number, and the answers to each question to our google sheet.

For a step by step walkthrough, follow the guide on
our [developer portal](https://developer.signalwire.com/guides/python-survey-with-google-sheets/).

# Configuring Google Sheets

You must first configure the google sheet that will receive your data.

<img width="1496" alt="Screen Shot 2021-04-14 at 2 19 47 PM" src="https://user-images.githubusercontent.com/58792902/114766802-7c08b780-9d2c-11eb-8624-dde609518c7a.png">

# Configuring Google Cloud Platform

Google Cloud Platform is next on the list of things to set up before we can use our Python script. Google Cloud
Platform (GCP) offers a myriad of cloud computing services, but we will be using the Google Sheets API so that our
application can connect with the google sheet.

![Screen Shot 2021-04-14 at 2 24 50 PM](https://user-images.githubusercontent.com/58792902/114767565-6778ef00-9d2d-11eb-9703-9ecfcac9b4f8.png)

Create a new GCP project and add both Google Drive and the Google Sheets API. Once complete, go to **APIs & Services**
and click **Credentials** instead. Click the blue + button at the top that says **CREATE CREDENTIALS** next to it and
choose the option **Help Me Choose**.

You will need to answer a few questions, which are stated in bold and answered directly below.

**What API are you using?**
Google Drive API

**Where will you be calling the API from?**
Web server (e.g. node.js, Tomcat) In our case, this will be Flask!

**What data will you be accessing?**
Application Data

**Are you planning to use this API with App Engine or Compute Engine?**
No, I'm not using them.

Next, click **What credentials do I need?**

This will open the **Create a service account** section. After creating your service account, scroll down to the **
Project** section under **All Roles** which will display some extra options on the right side. Select **Editor** here.
Make sure to select **JSON** as the key type and select continue. This should trigger a JSON file to be downloaded on
your browser.

Open the JSON file in a text editor and copy whatever the value of the `client_email` key is. Now we need to go back to
the Google Sheet that was created, click on the **Share** button, paste the copied email address, assign the role of **
Editor** to that email address, and click send!

## What do I need to run this code?

Follow the steps above or in the article to configure your google sheet and Google Cloud Platform. You will need the
Flask framework and the
SignalWire [Python SDK](https://docs.signalwire.com/topics/laml-api/#laml-rest-api-client-libraries-and-sdks-python)
downloaded.

# How to Run Application

To run the application, execute `export FLASK_APP=covid_survey.py` then run `flask run`.

You may need to use an SSH tunnel for testing this code – we recommend [ngrok](https://ngrok.com/). After starting the
tunnel, you can use the URL you receive from `ngrok` in your webhook configuration for your phone number.

You can use this application as both an inbound or outbound survey. If you want to use this as an inbound survey, put
the code on an accessible server use a webhook to the script as your webhook for handling incoming calls under phone
number settings. For example, this is what it looks like if you use an ngrok tunnel to the script.

![Screen Shot 2021-04-14 at 3 25 36 PM](https://user-images.githubusercontent.com/58792902/114774311-aca11f00-9d35-11eb-97f1-cae646f056bc.png)

Alternatively, you can send this as an outbound survey as well. You would do that by creating a call normally and using
the webhook to this script as the Url, like below:

```curl
curl https://example.signalwire.com/api/laml/2010-04-01/Accounts/{ProjectSid}/Calls.json \
  -X POST \
  --data-urlencode "Url=http://342jds746afd89.ngrok.io/survey/welcome" \
  --data-urlencode "To=+13105678901" \
  --data-urlencode "From=+13103384645" \
  -u "YourProjectID:YourAuthToken"
```

# Sign Up Here

If you would like to test this example out, you can create a SignalWire account and
space [here](https://m.signalwire.com/signups/new?s=1).

Please feel free to reach out to us on our [Community Slack](https://signalwire.community/) or create a Support ticket
if you need guidance!