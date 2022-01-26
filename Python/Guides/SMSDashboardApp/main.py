from flask import Flask, render_template, request, redirect
from signalwire.rest import Client as signalwire_client
import pandas as pd
import os
from dotenv import load_dotenv
import csv
import logging
import short_url
from datetime import datetime, date
import time
import datetime
import json
import requests
from requests.auth import HTTPBasicAuth

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

undeliveredArray = []

# import client
client = signalwire_client(projectID, authToken, signalwire_space_url=spaceURL)


# list all available numbers on account
def list_account_numbers():
    incoming_phone_numbers = client.incoming_phone_numbers.list()
    numbers = {}

    for record in incoming_phone_numbers:
        numbers[record.phone_number] = record.sid

    print(numbers)
    return numbers


# create a new number group
def create_number_group(groupName):
    url = f"https://{spaceURL}/api/relay/rest/number_groups"

    payloads = {
        'name': groupName,
        'sticky_sender': 'true'
    }

    payloadJSON = json.dumps(payloads)

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, headers=headers, data=payloadJSON,
                                auth=HTTPBasicAuth(projectID, authToken))
    print(f"Creating Number Group - details below")
    print(response.text)


# list number groups
def list_number_groups():
    url = f"https://{spaceURL}/api/relay/rest/number_groups"

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.request("GET", url, headers=headers, auth=HTTPBasicAuth(projectID, authToken))
    print(f"Listing number groups - details below")
    response_json = response.json()['data']
    print(response_json)
    return response_json


# list number groups
def list_number_group_members(groupID):
    url = f"https://{spaceURL}/api/relay/rest/number_groups/{groupID}/number_group_memberships"

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.request("GET", url, headers=headers, auth=HTTPBasicAuth(projectID, authToken))
    print(f"Listing number group members - details below")
    response_json = response.json()['data']
    print(response_json)
    return response_json


# add a number to a number group
def add_numbers_to_number_group(number, groupID):
    url = f"https://{spaceURL}/api/relay/rest/number_groups/{groupID}/number_group_memberships"

    # get sid of phone number
    numbers = list_account_numbers()
    numberID = numbers[number]

    payloads = {'phone_number_id': numberID}
    payloadJSON = json.dumps(payloads)

    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payloadJSON,
                                auth=HTTPBasicAuth(projectID, authToken))
    print(f"Adding {number} to number group {groupID}")
    print(response.text)


# BULK SEND SECTION BASED ON CSV FROM CUSTOMER DATA DIRECTORY
# looks in src folder by default - remove folder and allow choose from computer on browser
def send_in_bulk(fileName, body, nameIntro=False, optOut=False, numberGroupID=None):
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

        if numberGroupID:
            print("Using number group instead")
            # send message
            message = client.messages.create(
                messaging_service_sid=numberGroupID,
                body=f"{nameIntro} {body} {optOutLanguage}",
                to=formattedNumber)

            logging.info(
                'SID: {}, From: {}, To: {}, Body: {}, Date/Time Sent: {}'.format(message.sid, message.from_, message.to,
                                                                                 message.body, message.date_sent))
            # sleep for 1 second in order to rate limit at 1 messag per second - adjust based on your approved campaign throughput
            time.sleep(1)

        else:
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
        return message.sid


def formatNumber(number):
    formattedNumber = "+" + str(number) if "+" not in str(number) else str(number)
    return str(formattedNumber)


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
    return message.sid, message.from_, message.to, message.body, message.status, message.error_code, message.error_message, message.date_sent, message.direction, message.price, message.price_unit


# show message history for last 24 hours by default - use apply button on browser to pass additional parameters
def getMessageHistory():
    today = str(date.today())
    year = int(today[0:4])
    mon = int(today[5:7])
    day = int(today[8:10]) - 1


    messages = client.messages.list(date_sent_after=datetime.datetime(year, mon, day, 0, 0, 0))
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


getMessageHistory()


# remove customer row from CSV
def deleteCustomerDataCSV(folder, number, path=None):
    dir_list = os.listdir(folder)

    # remove opt out list from CSVs to evaluate
    for file in dir_list:
        if file == 'opted_out_customers.csv':
            dir_list.pop(dir_list.index(file))

    numCSVs = len(dir_list)
    i = 0

    if path:
        print(path)
        df = pd.read_csv(path)
        print("Before")
        print(df)
        nf = df.drop(df.index[df['Number'] == int(number)].tolist())
        print("After")
        print(nf)
        nf['Number'] = nf['Number'].apply(formatNumber)
        nf.to_csv(path, index=None)
        print(f"Customer associated with {number} removed from active customer data. \n")

    else:
        # loop through each CSV and delete rows with matching phone numbers
        while i < numCSVs:
            print(f"src/{dir_list[i]}")
            df = pd.read_csv(f"src/{dir_list[i]}")
            if int(number) in df.values:
                print("Before")
                print(df)
                nf = df.drop(df.index[df['Number'] == int(number)].tolist())
                print()
                print("After")
                print(nf)
                nf['Number'] = nf['Number'].apply(formatNumber)
                nf.to_csv(f"src/{dir_list[i]}", index=None)
                print()
                print(f"Customer associated with {number} removed from active customer data. \n")

            else:
                print("Number not found in this customer list")

            i += 1

    return 200


# upload CSV from computer and add to customer Data, display available CSVs
def uploadCSV(path, newTitle):
    # upload file from somewhere on computer, front end will grab path using js library
    # strip whitespace and convert to E164 format
    df = pd.read_csv(path, header=0)
    fileName = newTitle.replace(" ", "_") + '.csv'
    df = df.rename(columns=lambda x: x.strip())
    df['Number'] = df['Number'].apply(formatNumber)
    df.to_csv(f"src/{fileName}", index=False, encoding='utf-8')
    print("Newly uploaded CSV")
    print(df)
    print()

    # read in CSV to dict where phone number is the key and a list with [first name, last name, opt out date, and file] is the value
    results = {}
    with open('src/opted_out_customers.csv', 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            results[row['Number']] = [row['First'.strip()], row['Last'.strip()], row['Opt-Out-Date'.strip()],
                                      row['filename'.strip()]]
    print("Opt Out Dict")
    print(str(results))
    print()

    # loop through opt out dict and check if the phone number is in the recently uploaded CSV
    for result in results:
        if result in df.values:
            print(
                f"The number {result} in your most recent upload is associated with {results[result][0]} {results[result][1]} who opted out on {results[result][2]}. "
                f"They were originally uploaded in {results[result][3]}")

            numTries = 1
            while numTries < 4:
                decision = input('Do you want to remove this customer from the data you just uploaded? y/n \n')

                if decision.strip().lower() == 'y':
                    deleteCustomerDataCSV('src/', result, f"src/{fileName}")
                    break
                elif decision.strip().lower() == 'n':
                    print('Okay, but remember, ignoring opt outs is bad!')
                    break
                else:
                    if numTries == 3:
                        print("You entered input incorrectly too many times. "
                              "Skipping customer and checking for other opted out customers in recent upload. \n")
                        break
                    else:
                        print("Invalid Input. Please enter y for yes or n for no.")
                        print(f"{3 - numTries} tries left before customer removal is skipped.")
                        numTries += 1

    print("Finished looping through results")


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

    i = 0
    # loop through each CSV and look for a customer record with a matching number
    while i < numCSVs:
        with open(f"src/{dir_list[i]}", 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Number'] == number:
                    customerRecord.append([row['First'], row['Last'], row['Number'], today, f"{dir_list[i]}"])
        i += 1

    return customerRecord


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
        # date_sent = datetime.datetime.strptime(str(message.date_sent), "%Y-%m-%d %H:%M:%S%z")
        # if date_sent < yesterday:
        undeliveredArray.append(
            [message_sid, message_status, error_code, message.error_message, message.date_sent, message.to,
             message.from_, message.body])
        df = pd.DataFrame(undeliveredArray, columns=(
            'Message Sid', 'Message Status', 'Error Code', 'Error Message', 'DateSent', 'To', 'From', 'Body'))
        df['DateSent'] = pd.to_datetime(df['DateSent'])
        df = df.sort_values(by='DateSent', ascending=False)
        print(df.to_string())

    return ('', 200)


# handle inbound messages
@app.route('/inbound', methods=['POST'])
def inbound():
    message_body = request.values.get('Body', None)
    client_from = request.values.get('From', None)
    body = message_body.lower().strip()
    i = 0

    # opt out manager
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
                print("customer added to opt out list")

        # remove customer from customer data
        deleteCustomerDataCSV('src/', client_from)

    return client_from

# if __name__ == "__main__":
#     app.run(debug=True)

# test function calls
# send_in_bulk('test.csv', "Test from SignalWire", True, True)
# uploadCSV('/Users/cassiebowles/Documents/SignalWire/Python/Snippets/src/bulk_sms.csv', 'Tickets On Sale')
# displayCSV("/Users/cassiebowles/Documents/SignalWire/Python/Guides/SMSDashboardApp/src")
# generateShortenedURL('https://stackoverflow.com/questions/1497504/how-to-make-unique-short-url-with-python')
# getMessageHistory()
# deleteCustomerDataCSV('src/', '+19721111111', 'src/test.csv')
# uploadCSV('testing.csv', 'test2')
# create_number_group('Group1')
# list_number_groups()
# add_numbers_to_number_group('ff3ceddf-e1af-46cd-93ee-aaef1c36c30c', '9b530dd0-04ba-49d5-98e8-a3d7a80bee31')
# add_numbers_to_number_group('+19043445583', '9b530dd0-04ba-49d5-98e8-a3d7a80bee31')
# list_number_group_members('9b530dd0-04ba-49d5-98e8-a3d7a80bee31')
# send_in_bulk('test.csv', ' test')
# send_in_bulk('test.csv', ' test', nameIntro=True, optOut=True, numberGroupID='9b530dd0-04ba-49d5-98e8-a3d7a80bee31')
