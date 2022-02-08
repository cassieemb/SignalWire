from flask import Flask, render_template, request, redirect, flash, jsonify
from signalwire.rest import Client as signalwire_client
import pandas as pd
import os
from dotenv import load_dotenv
import csv
import logging
import short_url
from datetime import datetime, date, timedelta, timezone
import time
import datetime
import json
import requests
from requests.auth import HTTPBasicAuth
import numpy as np

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
load_dotenv()


# get environment variables from .env file
projectID = os.getenv('SIGNALWIRE_PROJECT')
authToken = os.getenv('SIGNALWIRE_TOKEN')
spaceURL = os.getenv('SIGNALWIRE_SPACE')
hostName = os.getenv('SIGNALWIRE_HOST_NAME')

# set upload folder for file upload
app.config['UPLOAD_FOLDER'] = 'src/'


# import client
client = signalwire_client(projectID, authToken, signalwire_space_url=spaceURL)


# list all available numbers on account
def list_account_numbers():
    incoming_phone_numbers = client.incoming_phone_numbers.list()
    numbers = {}

    for record in incoming_phone_numbers:
        numbers[record.phone_number] = record.sid

    return numbers


# assign inbound webhook to all phone numbers in project so that we can track stop replies
def assign_webhook():
    incoming_phone_numbers = client.incoming_phone_numbers.list()
    print("Total Numbers -- " + str(len(incoming_phone_numbers)))

    for record in incoming_phone_numbers:
        print("update number -- " + record.phone_number)
        response = requests.put(f"https://{spaceURL}/api/relay/rest/phone_numbers/" + record.sid,
                                params={'message_handler': 'laml_webhooks',
                                        'message_request_url': hostName + 'inbound'}
                                , auth=HTTPBasicAuth(projectID, authToken))
        print(response)


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
    return response.json()['id']


# create a new number group
def delete_number_group(groupID):
    url = f"https://{spaceURL}/api/relay/rest/number_groups/{groupID}"

    payloads = {}

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.request("DELETE", url, headers=headers, data=payloads, auth=HTTPBasicAuth(projectID, authToken))
    print(response)
    print(f"Deleting Number Group - details below")
    print(response.text)


# list number groups
def list_number_groups():
    url = f"https://{spaceURL}/api/relay/rest/number_groups"

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.request("GET", url, headers=headers, auth=HTTPBasicAuth(projectID, authToken))
    response_json = response.json()['data']

    # print(response_json)
    return response_json

# get number group name
def get_group_name(id):
    url = f"https://{spaceURL}/api/relay/rest/number_groups/{id}"

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.request("GET", url, headers=headers, auth=HTTPBasicAuth(projectID, authToken))
    response_json = response.json()['name']
    return response_json

# list number groups
def list_number_group_members(groupID):
    url = f"https://{spaceURL}/api/relay/rest/number_groups/{groupID}/number_group_memberships"

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.request("GET", url, headers=headers, auth=HTTPBasicAuth(projectID, authToken))
    response_json = response.json()['data']

    groupMembers = []
    for response in response_json:
        memberDict = response['phone_number']
        groupMembers.append(memberDict)

    return groupMembers


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
def send_in_bulk(fileName, body, nameIntro=False, optOut=False, numberGroupID=None, fromNumber=None):
    # define results dict for storing client records from csv
    results = {}

    # read in CSV to dict where phone number is the key and [first name, last name] is the value
    with open(f"src/{fileName}", 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            results[row['Number']] = [row['First'], row['Last']]

    # if using number group to send
    if numberGroupID:
        sendType = 'Number Group'
        for customer in results:
            # change formatted number to E164, change nameIntro to Hello Name if true, change optOutLanuage to reply stop to opt out if true
            formattedNumber = "+" + customer if "+" not in customer else customer
            nameIntro = f"Hello {results[str(customer)][0]}," if nameIntro else ""
            optOutLanguage = "Reply Stop to Opt Out" if optOut else ""

            # send message
            message = client.messages.create(
                messaging_service_sid=numberGroupID,
                body=f"{nameIntro} {body} {optOutLanguage}",
                to=formattedNumber,
                status_callback=f"{hostName}statusCallbacks"
            )

            logging.info(
                'SID: {}, From: {}, To: {}, Body: {}, Date/Time Sent: {}'.format(message.sid, message.from_, message.to,
                                                                                 message.body, message.date_sent))
            # sleep for 1 second in order to rate limit at 1 messag per second - adjust based on your approved campaign throughput
            time.sleep(1)

    # if using one account number to send
    else:
        sendType = 'Account Number'
        for customer in results:
            # change formatted number to E164, change nameIntro to Hello Name if true, change optOutLanuage to reply stop to opt out if true
            formattedNumber = "+" + customer if "+" not in customer else customer
            nameIntro = f"Hello {results[str(customer)][0]}," if nameIntro else ""
            optOutLanguage = "Reply Stop to Opt Out" if optOut else ""

            # send message
            message = client.messages.create(
                from_=fromNumber,
                body=f"{nameIntro} {body} {optOutLanguage}",
                to=formattedNumber,
                status_callback=f"{hostName}statusCallbacks"
            )

            logging.info(
                'SID: {}, From: {}, To: {}, Body: {}, Date/Time Sent: {}'.format(message.sid, message.from_, message.to,
                                                                                 message.body, message.date_sent))
            # sleep for 1 second in order to rate limit at 1 messag per second - adjust based on your approved campaign throughput
            time.sleep(1)

    # update sends.csv with new send data
    df = pd.read_csv('src/sends.csv')

    if nameIntro:
        nameIntro = True
    else:
        nameIntro = False

    if optOut:
        optOut = True
    else:
        optOut = False

    df.loc[len(df.index)] = [datetime.date.today(), fileName, len(results), sendType, nameIntro, optOut]

    df['Send Date'] = pd.to_datetime(df['Send Date'], utc=True)
    df = df.sort_values(by='Send Date', ascending=False)
    df.replace({np.nan: None})
    df.to_csv('src/sends.csv', index=None)

    return

# format numbers
def formatNumber(number):
    formattedNumber = "+" + str(number) if "+" not in str(number) else str(number)
    return str(formattedNumber)


# generate shortened URL using encoding and store in CSV
def generateShortenedURL(fullURL, keyword):
    # read in csv using pandas
    shortenedUrls = pd.read_csv('src/shortUrls.csv')
    object_id = len(shortenedUrls)

    shortened_url = f"{hostName}{keyword}/{short_url.encode_url(object_id, min_length=3)}"
    shortenedUrls.loc[len(shortenedUrls.index)] = [fullURL, shortened_url, datetime.date.today(), 'Not Used Yet', 0]
    shortenedUrls.to_csv('src/shortUrls.csv', index=None)
    return shortened_url


# delete shortened URL from CSV
def deleteShortenedURL(fullURL):
    # read in csv using pandas
    shortenedUrls = pd.read_csv('src/shortUrls.csv')

    # delete row with matching fullURL
    shortenedUrls.drop(shortenedUrls[shortenedUrls['Full URL'] == fullURL].index, inplace=True)
    shortenedUrls.to_csv('src/shortUrls.csv', index=None)
    return 'shortened URL deleted'


# pull message details using SID
def pullMessage(sid):
    message = client.messages(sid).fetch()

    return message.sid, message.from_, message.to, message.body, message.status, message.error_code, message.error_message, message.date_sent, message.direction, message.price, message.price_unit


# show message history for last 24 hours by default
def getMessageHistory(startDate=None, endDate=None, fromN=None, toN=None):
    # if no startDate is passed as args, assign default start date as the beginning of the previous date
    if not startDate:
        today = str(date.today())
        year = int(today[0:4])
        mon = int(today[5:7])
        day = int(today[8:10])
        startDate = datetime.datetime(year, mon, day)
    else:
        year = int(startDate[0:4])
        mon = int(startDate[5:7])
        day = int(startDate[8:10])

        startDate = datetime.datetime(year, mon, day)

    # if end date is passed in, parse into datetime here
    if endDate:
        year = int(endDate[0:4])
        mon = int(endDate[5:7])
        day = int(endDate[8:10])
        endDate = datetime.datetime(year, mon, day)

    # if from number is passed in, format in E164
    if fromN:
        fromN = formatNumber(fromN)

    # if to number is passed in, format in E164
    if toN:
        toN = formatNumber(toN)
    messages = client.messages.list(date_sent_after=startDate, date_sent_before=endDate, from_=fromN, to=toN)

    d = []
    for record in messages:
        d.append((record.from_, record.to, record.date_sent, record.status, record.sid, record.direction,
                  record.error_message, record.price))
        pullMessage(record.sid)

    # format price and sort by most recent date
    df = pd.DataFrame(d, columns=('From', 'To', 'Date', 'Status', 'SID', 'Type', 'Message Error', 'Price'))
    df['Price'] = df['Price'].fillna(0)
    df['Price'] = df['Price'].astype(float).round(4)
    df['Price'] = df['Price'].map('${:,.4f}'.format)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date', ascending=False)
    # print(df.to_string())
    return df


# show failed or undelivered messages filtered by any parameters
def showMessageFailures(status, dateSentAfter=None, dateSentBefore=None):
    url = f"https://{spaceURL}/api/laml/2010-04-01/Accounts/{projectID}/Messages.json?PageSize=500&Status={status}&DateSent<={dateSentBefore}&DateSent>={dateSentAfter}"

    payload = {}
    headers = {
    }

    response = requests.request("GET", url, headers=headers, data=payload, auth=HTTPBasicAuth(projectID, authToken))

    messages = response.json()['messages']

    d = []
    for msg in messages:
        d.append((msg['from'], msg['to'], msg['date_sent'], msg['status'], msg['sid'], msg['direction'],
                  msg["error_message"], msg["error_code"]))

    # sort by most recent date
    df = pd.DataFrame(d, columns=('From', 'To', 'Date', 'Status', 'SID', 'Type', 'Message Error', 'Error Code'))
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date', ascending=False)

    return df


# remove customer row from CSV
def deleteCustomerDataCSV(folder, number, path=None):
    dir_list = os.listdir(folder)

    # remove opt out list from CSVs to evaluate
    for file in dir_list:
        if file == 'opt_out_list.csv':
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


# display all existing CSVs
def displayCSV(path):
    # show available CSVs and their contents
    dir_list = os.listdir(path)

    # remove failed messages and short URLs from list
    for file in dir_list:
        if file == 'failedMessages.csv':
            dir_list.pop(dir_list.index(file))

    for file in dir_list:
        if file == 'shortUrls.csv':
            dir_list.pop(dir_list.index(file))

    for file in dir_list:
        if file == 'sends.csv':
            dir_list.pop(dir_list.index(file))

    numCSVs = len(dir_list)
    i = 0
    results = {}

    while i < numCSVs:
        with open(f"src/{dir_list[i]}", 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                results[row['Number']] = [row['First'], row['Last']]
        i += 1
    return dir_list


# search CSV and return customer record if it exists
def searchCSV(path, number):
    dir_list = os.listdir(path)

    # remove opt out list from CSVs to evaluate
    for file in dir_list:
        if file == 'opt_out_list.csv':
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


# grab CSV file and load into customer data table
def dropdownCSVTable(filename):
    fileName = f"src/{filename}"
    data = pd.read_csv(fileName)
    customerList = list(data.values)
    return customerList


# handle inbound shortened url requests and redirect to full URL
@app.route("/<name>/<char>", methods=('GET', 'POST'))
def redirectShortCode(char, name):
    decoded_id = short_url.decode_url(char)
    shortenedUrls = pd.read_csv('src/shortUrls.csv')
    fullURL = shortenedUrls.loc[decoded_id, 'Full URL']
    shortenedUrls.loc[decoded_id, 'Last Clicked'] = datetime.date.today()
    shortenedUrls.loc[decoded_id, 'Times Clicked'] = shortenedUrls.loc[decoded_id, 'Times Clicked'] + 1
    shortenedUrls.to_csv('src/shortUrls.csv', index=None)

    return redirect(fullURL, code=302)


# handle status callbacks
@app.route("/statusCallbacks", methods=('GET', 'POST'))
def status_callbacks():
    message_sid = request.values.get('MessageSid', None)
    message_status = request.values.get('MessageStatus', None)
    error_code = request.values.get('ErrorCode', None)
    logging.info('SID: {}, Status: {}, ErrorCode: {}'.format(message_sid, message_status, error_code))

    df = pd.read_csv('src/failedMessages.csv')

    if (message_status == "undelivered" or message_status == "failed"):
        message = client.messages(message_sid).fetch()
        df.loc[len(df.index)] = [message_sid, message_status, error_code, message.error_message, message.date_sent,
                                 message.to,
                                 message.from_, message.body]

    df['DateSent'] = pd.to_datetime(df['DateSent'], utc=True)
    df = df.sort_values(by='DateSent', ascending=False)
    df.to_csv('src/failedMessages.csv', index=None)

    return '200'


# error center for displaying the failed or undelivered messages
@app.route('/errorCenter', methods=('GET', 'POST'))
def errorCenter():
    if request.form.get('status'):
        status = request.form.get('status')

        if request.form.get('DateSentAfter'):
            dateSentAfter = request.form.get('DateSentAfter')

            if request.form.get('DateSentBefore'):
                dateSentBefore = request.form.get('DateSentBefore')

                df = showMessageFailures(status, dateSentAfter=dateSentAfter, dateSentBefore=dateSentBefore)
                table = df.to_html(
                    classes=["table", "table-striped", "table-dark", "table-hover", "table-condensed", "table-fixed"],
                    index=False)

            else:
                df = showMessageFailures(status, dateSentAfter)
                table = df.to_html(
                    classes=["table", "table-striped", "table-dark", "table-hover", "table-condensed", "table-fixed"],
                    index=False)

        else:
            if request.form.get('DateSentBefore'):
                dateSentBefore = request.form.get('DateSentBefore')
                df = showMessageFailures(status, dateSentBefore=dateSentBefore)
                table = df.to_html(
                    classes=["table", "table-striped", "table-dark", "table-hover", "table-condensed", "table-fixed"],
                    index=False)

            else:
                df = showMessageFailures(status)
                table = df.to_html(
                    classes=["table", "table-striped", "table-dark", "table-hover", "table-condensed", "table-fixed"],
                    index=False)

    else:
        df = pd.read_csv('src/failedMessages.csv')
        table = df.to_html(
            classes=["table", "table-striped", "table-dark", "table-hover", "table-condensed", "table-fixed"],
            index=False)

    return render_template('errorCenter.html', table=table)


# handle inbound messages
@app.route('/inbound', methods=('GET', 'POST'))
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
        with open('src/opt_out_list.csv', 'a') as f:
            writer = csv.writer(f)
            while i < len(opt_out_record):
                writer.writerow(opt_out_record[i])
                i += 1
                print("customer added to opt out list")

        # remove customer from customer data
        deleteCustomerDataCSV('src/', client_from)

    return client_from


# handle home page requests
@app.route("/home", methods=('GET', 'POST'))
def home():
    return render_template('index.html')


# handle customer data home page requests
@app.route("/customerData", methods=('GET', 'POST'))
def customerData():
    if request.args.get('filename'):
        fileName = request.args.get('filename')

    else:
        fileName = 'opt_out_list.csv'

    fileNamePath = f"src/{fileName}"
    data = pd.read_csv(fileNamePath)

    csvList = displayCSV('src/')

    return render_template('customerData.html', csvs=csvList, tableName = fileName,
                           table=data.to_html(classes=["table", "table-striped", "table-dark"], index=False))


# handle number group page requests
@app.route('/numberGroups', methods=('GET', 'POST'))
def numberGroups():
    h4 = ''
    groupName = 'None Selected'
    # handle add number to number group requests
    if request.args.get('numbers'):
        numbers = request.args.getlist('numbers')

        if request.args.get('chosenGroup'):
            groupID = request.args.get('chosenGroup')

            for number in numbers:
                add_numbers_to_number_group(number, groupID)

            return redirect(f"/numberGroups?id={groupID}")

    # handle delete number group requests
    if request.args.get('delGroup'):
        delete_number_group(request.args.get('delGroup'))

    # handle create new group requests
    if request.args.get('newGroupName'):
        ngID = create_number_group(request.args.get('newGroupName'))
        return redirect(f"/numberGroups?id={ngID}")

    # load available number groups and account numbers
    groups = list_number_groups()
    numbers = list_account_numbers()

    # load empty table and set h4 to alert if there are no number groups
    if (len(groups) == 0):
        h4 = "You don't have any number groups! Create a group and then add numbers to it."
        d = []
        data = pd.DataFrame(d, columns=('id', 'name', 'number', 'capabilities'))
        group_table = data.to_html(classes=["table", "table-striped", "table-dark"], index=False)

    # load specific number group results
    elif request.args.get('id'):

        id = request.args.get('id')
        memberData = json.dumps(list_number_group_members(id))
        print(memberData)
        data = pd.read_json(memberData)
        group_table = data.to_html(classes=["table", "table-striped", "table-dark"], index=False)
        groupName = get_group_name(id)

        if len(data) == 0:
            h4 = 'This number group is empty! Add numbers to it now to see them below.'
            d = []
            data = pd.DataFrame(d, columns=('id', 'name', 'number', 'capabilities'))
            group_table = data.to_html(classes=["table", "table-striped", "table-dark"], index=False)

    # load empty table and set h4 to direct to click a number group
    else:
        d = []
        data = pd.DataFrame(d, columns=('id', 'name', 'number', 'capabilities'))
        group_table = data.to_html(classes=["table", "table-striped", "table-dark"], index=False)
        h4 = "Click a number group from the left to see the numbers it contains below."

    return render_template('numberGroups.html', groups=groups, table=group_table, groupName = groupName, numbers=numbers, h4=h4)


# handle data upload requests
@app.route('/uploadFile', methods=('GET', 'POST'))
def uploadFileChoice():
    if request.method == 'POST' and 'file' in request.files:
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        filename = f.filename

        # read in newly created CSV and format phone number
        df = pd.read_csv(f"src/{filename}", header=0)
        newPath = f"src/{filename}"
        df = df.rename(columns=lambda x: x.strip())
        df['Number'] = df['Number'].apply(formatNumber)
        df.to_csv(newPath, index=False, encoding='utf-8')
        print("Newly uploaded CSV")
        print(df)

        # read in CSV to dict where phone number is the key and a list with [first name, last name, opt out date, and file] is the value
        results = {}
        with open('src/opt_out_list.csv', 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                results[row['Number']] = [row['First'.strip()], row['Last'.strip()], row['Opt-Out-Date'.strip()],
                                          row['filename'.strip()]]
        print("Opt Out Dict")
        print(str(results))

        # loop through opt out dict and check if the phone number is in the recently uploaded CSV
        for result in results:
            if result in df.values:
                print(f"The number {result} in your most recent upload is associated with {results[result][0]} "
                      f"{results[result][1]} who opted out on {results[result][2]}. "
                    f"They were originally uploaded in {results[result][3]}")

                numTries = 1
                while numTries < 4:
                    decision = input('Do you want to remove this customer from the data you just uploaded? y/n \n')

                    if decision.strip().lower() == 'y':
                        deleteCustomerDataCSV('src/', result, f"src/{filename}")
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

    else:
        filename = None
    return redirect(f"/customerData?filename={filename}", code=302)


# handle message history requests
@app.route('/messageHistory', methods=['POST', 'GET'])
def messageHistory():
    if request.form.get('startDate'):
        startDate = request.form.get('startDate')
    else:
        startDate = None

    if request.form.get('endDate'):
        endDate = request.form.get('endDate')
    else:
        endDate = None

    if request.form.get('from'):
        fromN = request.form.get('from')
    else:
        fromN = None

    if request.form.get('to'):
        toN = request.form.get('to')
    else:
        toN = None

    data = getMessageHistory(startDate=startDate, endDate=endDate, fromN=fromN, toN=toN)

    return render_template('messageHistory.html', table=data.to_html(
        classes=["table", "table-striped", "table-dark", "table-hover", "table-condensed", "table-fixed"], index=False))


# handle url shortener
@app.route('/shortUrls', methods=['POST', 'GET'])
def shortenedURLs():
    # generate new shortened URL
    if request.args.get('fullURL'):
        fullURL = request.args.get('fullURL')
        if request.args.get('keyword'):
            keyword = request.args.get('keyword')
            generateShortenedURL(fullURL, keyword)
        else:
            keyword = 'sc'
            generateShortenedURL(fullURL, keyword)

    # delete shortened URL
    if request.args.get('delURL'):
        delURL = request.args.get('delURL')
        deleteShortenedURL(delURL)

    data = pd.read_csv('src/shortUrls.csv')
    urls = data['Full URL'].tolist()

    return render_template('urlShortener.html', table=data.to_html(
        classes=["table", "table-striped", "table-dark", "table-hover", "table-condensed", "table-fixed"], index=False),
                           urls=urls)


# handle  bulk messaging
@app.route('/textBlasts', methods=['POST', 'GET'])
def bulkSend():
    csvList = displayCSV('src/')
    groups = list_number_groups()
    numbers = list_account_numbers()

    if request.args.get('body'):
        body = request.args.get('body')
        filename = request.args.get('filename')

        if request.args.get('optOut'):
            optOut = request.args.get('optOut')
        else:
            optOut = False

        if request.args.get('nameIntro'):
            nameIntro = request.args.get('nameIntro')
        else:
            nameIntro = False

        if request.args.get('fromNumber') != None:
            fromNumber = request.args.get('fromNumber')
            groupID = None
        else:
            fromNumber = None
            groupID = request.args.get('groupID')

        send_in_bulk(filename, body, nameIntro, optOut, groupID, fromNumber)

    data = pd.read_csv('src/sends.csv')
    return render_template('bulkSend.html', csvs=csvList, groups=groups, numbers=numbers, table=data.to_html(
        classes=["table", "table-striped", "table-dark", "table-hover", "table-condensed", "table-fixed"], index=False))


if __name__ == "__main__":
    # assign_webhook()
    app.run(debug=True)
