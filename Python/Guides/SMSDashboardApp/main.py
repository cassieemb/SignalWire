from flask import Flask, render_template, request, redirect
from signalwire.rest import Client as signalwire_client
import pandas as pd
import os
from dotenv import load_dotenv
import csv
import logging
import short_url
from datetime import datetime, timedelta, date
import time
import datetime
import json
import dateutil
import tz


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
load_dotenv()

# get environment variables from .env file
projectID = os.getenv('SIGNALWIRE_PROJECT')
authToken = os.getenv('SIGNALWIRE_TOKEN')
spaceURL = os.getenv('SIGNALWIRE_SPACE')
fromNumber = os.getenv('SIGNALWIRE_FROM_NUMBER')
hostName = os.getenv('SIGNALWIRE_HOST_NAME')

# dictionary of shortened URLs that can be displayed
shortenedUrls = {}

# today = datetime.datetime.today()
# yesterday = today - timedelta(days=1)
# tf = yesterday.strftime(f"%Y-%m-%d %H:%M:%S%z")
# one_week_ago = today - timedelta(days=7)
# thirty_days_ago = today - timedelta(days=30)

undeliveredArray = []

# import client
client = signalwire_client(projectID, authToken, signalwire_space_url=spaceURL)

# functions necessary to perform requests
# BULK SEND SECTION BASED ON CSV FROM CUSTOMER DATA DIRECTORY
def send_in_bulk(fileName, body, nameIntro, optOut):
    # define results dict for storing client records from csv
    results = {}

    # read in CSV to dict where phone number is the key and [first name, last name] is the value
    with open(f"src/{fileName}", 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            results[row['Number']] = [row['First'], row['Last']]

    for customer in results:
        # change formatted number to E164, change nameIntro to Hello Name if true, change optOutLanuage to reply stop to opt out if true
        formattedNumber = "+" + customer if "+" not in customer else customer
        nameIntro = f"Hello {results[str(customer)][0]}," if nameIntro else ""
        optOutLanguage = "Reply Stop to Opt Out" if optOut else ""

        # send message
        message = client.messages.create(
            from_=fromNumber,
            body=f"{nameIntro} {body} {optOutLanguage}",
            to=formattedNumber)

        logging.info(
            'SID: {}, From: {}, To: {}, Body: {}, Date/Time Sent: {}'.format(message.sid, message.from_, message.to,
                                                                             message.body, message.date_sent))
        # sleep for 1 second in order to rate limit at 1 messag per second - adjust based on your approved campaign throughput
        time.sleep(1)

def formatNumber(number):
    formattedNumber = "+" + str(number) if "+" not in str(number) else str(number)
    return str(formattedNumber)

# upload CSV from computer and add to customer Data, display available CSVs
def uploadCSV(path, newTitle):
    # upload file from somewhere on computer, front end will grab path using js library
    df = pd.read_csv(path)
    fileName = newTitle.replace(" ", "_") + '.csv'
    df['Number'] = df['Number'].apply(formatNumber)
    df.to_csv(f"src/{fileName}", index=False, encoding='utf-8')


# display all existing CSVs
def displayCSV(path):
    # print available CSVs
    dir_list = os.listdir(path)
    print(dir_list)
    numCSVs = len(dir_list)
    print(numCSVs)
    i = 0
    results = {}

    while i < numCSVs:
        print(dir_list[i])
        with open(f"src/{dir_list[i]}", 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                results[row['Number']] = [row['First'], row['Last']]
        i += 1
        print(results)
    return results

# generate shortened URL using encoding and store in dictionary
def generateShortenedURL(fullURL):
    # generate shortened URL from full URL
    object_id = len(shortenedUrls)
    shortened_url = f"{hostName}sc/{short_url.encode_url(object_id, min_length=6)}"
    # store in shortened URL dictionary
    shortenedUrls[shortened_url] = fullURL

# pull message details using SID for alert box
def pullMessage(sid):
    message = client.messages(sid).fetch()
    return message.sid, message.from_, message.to, message.body, message.status, message.error_code, message.error_message, message.date_sent, message.direction, message.price,message.price_unit

# message history section
# show history default last 7 days when loading browser page, refresh results every 1 minute on page, click filter page to fill out additional parameters and return messages
# click sid to show alert box with additional message details and apply button
def getMessageHistory():
    messages = client.messages.list()
    d = []
    for record in messages:
        d.append((record.from_, record.to, record.date_sent, record.status, record.sid, record.price,
                  record.direction))
        pullMessage(record.sid)

    # format price and sort by most recent date
    df = pd.DataFrame(d, columns=('From', 'To', 'Date', 'Status', 'SID', 'Price', 'Type'))
    df['Price'] = df['Price'].fillna(0)
    df['Price'] = df['Price'].astype(float).round(4)
    df['Price'] = df['Price'].map('${:,.4f}'.format)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date', ascending=False)
    print(df.to_string())

# search CSV and return customer record if it exists
def searchCSV(path, number):
    dir_list = os.listdir(path)

    # remove opt out list from CSVs to evaluate
    for file in dir_list:
        if file == 'opted_out_customers.csv':
             dir_list.pop(dir_list.index(file))

    numCSVs = len(dir_list)
    today = str(date.today())

    # create customer record list to store any matching records
    customerRecord = []

    # remove + in case subscriber info doesn't have it
    unformattedNumber = number.replace('+', '') if "+" in number else number

    i = 0
    # loop through each CSV and look for a customer record with a matching number
    while i < numCSVs:
        with open(f"src/{dir_list[i]}", 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Number'] == number or row['Number'] == unformattedNumber:
                    customerRecord.append([row['First'], row['Last'], row['Number'], today, f"{dir_list[i]}"])
        i += 1

    return customerRecord

# remove customer row from CSV
def deleteCustomerDataCSV(path, number):
    dir_list = os.listdir(path)

    # remove opt out list from CSVs to evaluate
    for file in dir_list:
        if file == 'opted_out_customers.csv':
             dir_list.pop(dir_list.index(file))

    numCSVs = len(dir_list)

    i = 0
    # loop through each CSV and delete rows with matching phone numbers
    while i < numCSVs:
        df = pd.read_csv(f"src/{dir_list[i]}")
        print(df)
        print()
        nf = df.drop(df.index[df['Number'] == int(number)].tolist())
        print(nf)
        print()
        i += 1

    return 200


# test function calls
# send_in_bulk('test.csv', "Test from SignalWire", True, True)
# uploadCSV('/Users/cassiebowles/Documents/SignalWire/Python/Snippets/src/bulk_sms.csv', 'Tickets On Sale')
# displayCSV("/Users/cassiebowles/Documents/SignalWire/Python/Guides/SMSDashboardApp/src")
# generateShortenedURL('https://stackoverflow.com/questions/1497504/how-to-make-unique-short-url-with-python')
# getMessageHistory()


# app routes
# handle inbound shortened url requests and redirect to full URL
@app.route("/sc/<char>", methods=('GET', 'POST'))
def redirectShortCode(char):
    decoded_id = short_url.decode_url(char)
    origURL = list(shortenedUrls.values())[decoded_id]
    return redirect(origURL, code=302)


# error code center using status callbacks to show failed messages, need to add some sort of time filter to limit results
# offer additional filters that can be implemented by hitting apply button
@app.route("/ErrorCenter", methods=['POST'])
def status_callbacks():
    message_sid = request.values.get('MessageSid', None)
    message_status = request.values.get('MessageStatus', None)
    error_code = request.values.get('ErrorCode', None)
    message_body = request.values.get('Body', None)
    logging.info('SID: {}, Status: {}, ErrorCode: {}'.format(message_sid, message_status, error_code))

    if (message_status == "undelivered" or message_status == "failed"):
        message = client.messages(message_sid).fetch()
        #date_sent = datetime.datetime.strptime(str(message.date_sent), "%Y-%m-%d %H:%M:%S%z")
        #if date_sent < yesterday:
        undeliveredArray.append([message_sid, message_status, error_code, message.error_message, message.date_sent, message.to, message.from_, message.body])
        df = pd.DataFrame(undeliveredArray, columns=(
        'Message Sid', 'Message Status', 'Error Code', 'Error Message', 'DateSent', 'To', 'From', 'Body'))
        df['DateSent'] = pd.to_datetime(df['DateSent'])
        df = df.sort_values(by='DateSent', ascending=False)
        print(df.to_string())

    return ('', 200)

# opt out manager
@app.route('/inbound', methods=['POST'])
def inbound():
    message_body = request.values.get('Body', None)
    client_from = request.values.get('From', None)
    body = message_body.lower().strip()
    i = 0


    # first handle opt outs
    if 'stop' in body or 'unsubscribe' in body:
        # search customer data for matching from number
        opt_out_record = searchCSV('src/', client_from)
        print(opt_out_record)
        # add to opted out user list
        with open('src/opted_out_customers.csv', 'a') as f:
            writer = csv.writer(f)
            while i < len(opt_out_record):
                writer.writerow(opt_out_record[i])
                i += 1
        # remove customer from customer data
        deleteCustomerDataCSV('src/', client_from)

    return client_from

if __name__ == "__main__":
    app.run(debug=True)


# set up number groups


# conversational messaging (UI showing OG messages where there is a reply in the last 7 days)
# log in page