from flask import Flask, render_template, request
from signalwire.rest import Client as signalwire_client
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

app = Flask(__name__)


def listAll(start, end):
    # will contain all messages and all calls in one dataframe
    callClient = signalwire_client("ProjectID",
                                   "AuthToken",
                                   signalwire_space_url='example.signalwire.com')

    messageClient = signalwire_client("ProjectID",
                                      "AuthToken",
                                      signalwire_space_url='example.signalwire.com')
    calls = callClient.calls.list(start_time_after=start,
                                  start_time_before=end)
    messages = messageClient.messages.list(date_sent_after=start,
                                           date_sent_before=end, )
    d = []

    for record in calls:
        d.append(
            (record.from_formatted, record.to_formatted, record.start_time, record.status, record.sid, record.price,
             record.direction + " call"))

    for record in messages:
        d.append((record.from_, record.to, record.date_sent, record.status, record.sid, record.price,
                  record.direction + " message"))

    # format dataframe
    df = pd.DataFrame(d, columns=('From', 'To', 'Date', 'Status', 'SID', 'Price', 'Type'))
    df['Price'] = df['Price'].fillna(0)
    df['Price'] = df['Price'].astype(float).round(4)
    df['Price'] = df['Price'].map('${:,.4f}'.format)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date', ascending=False)

    # format table with some html styling
    def hover(hover_color="lightblue"):
        return dict(selector="tr:hover",
                    props=[("background-color", "%s" % hover_color)])

    def highlightEven(even_color="lightgrey"):
        return dict(selector="tr:nth-child(even)",
                    props=[("background-color", "%s" % even_color)])

    th_props = [('padding-top', '12px'),
                ('padding-bottom', '12px'),
                ('text-align', 'center'),
                ('background-color', '#add8e6'),
                ('border', 'solid black')
                ]

    tr_props = [('padding-top', '12px'),
                ('padding-bottom', '12px'),
                ('text-align', 'center'),
                ('border', 'solid black')
                ]

    td_props = [('padding-top', '12px'),
                ('padding-bottom', '12px'),
                ('text-align', 'center'),
                ('border', 'solid black')
                ]

    caption_props = [('caption-side', 'top'),
                     ("font-size", "200%"),
                     ("text-align", "center"),
                     ("font", "bold")
                     ]

    styles = [
        hover(),
        highlightEven(),
        dict(selector="caption", props=caption_props),
        dict(selector='', props=[("border-collapse", "collapse")]),
        dict(selector='tr', props=tr_props),
        dict(selector='td', props=td_props),
        dict(selector='th', props=th_props),

    ]
    html = (df.style
            .set_table_styles(styles)
            .hide_index()
            .set_caption("All Communications Reporting - Hover to Highlight a Record.")
            .render())

    return html


def listMessages(start, end):
    # offer ability to filter by date
    messageClient = signalwire_client("0ea23c2c-6b11-4154-b3f3-49bd702936dd",
                                      "PT73051c323c68732cd9a0b1480b920d612b4c3bda3ca800c7",
                                      signalwire_space_url='bowl-test.signalwire.com')

    messages = messageClient.messages.list(date_sent_after=start,
                                           date_sent_before=end, )
    d = []

    for record in messages:
        d.append((record.from_, record.to, record.date_sent, record.status, record.sid, record.price,
                  record.direction))

    # format dataframe
    df = pd.DataFrame(d, columns=('From', 'To', 'Date', 'Status', 'Message SID', 'Price', 'Direction'))
    df['Price'] = df['Price'].fillna(0)
    df['Price'] = df['Price'].astype(float).round(4)
    df['Price'] = df['Price'].map('${:,.4f}'.format)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date', ascending=False)

    # format table with some html styling
    def hover(hover_color="lightblue"):
        return dict(selector="tr:hover",
                    props=[("background-color", "%s" % hover_color)])

    def highlightEven(even_color="lightgrey"):
        return dict(selector="tr:nth-child(even)",
                    props=[("background-color", "%s" % even_color)])

    th_props = [('padding-top', '12px'),
                ('padding-bottom', '12px'),
                ('text-align', 'center'),
                ('background-color', '#add8e6'),
                ('border', 'solid black')
                ]

    tr_props = [('padding-top', '12px'),
                ('padding-bottom', '12px'),
                ('text-align', 'center'),
                ('border', 'solid black')
                ]

    td_props = [('padding-top', '12px'),
                ('padding-bottom', '12px'),
                ('text-align', 'center'),
                ('border', 'solid black')
                ]

    caption_props = [('caption-side', 'top'),
                     ("font-size", "200%"),
                     ("text-align", "center"),
                     ("font", "bold")
                     ]

    styles = [
        hover(),
        highlightEven(),
        dict(selector="caption", props=caption_props),
        dict(selector='', props=[("border-collapse", "collapse")]),
        dict(selector='tr', props=tr_props),
        dict(selector='td', props=td_props),
        dict(selector='th', props=th_props),

    ]
    html = (df.style
            .set_table_styles(styles)
            .hide_index()
            .set_caption("Message Reporting - Hover to Highlight a Record.")
            .render())

    return html


def listCalls(start, end):
    # offer ability to filter by date, to, or from
    callClient = signalwire_client("e8f48a64-d62b-4bd5-a8d6-b26824a19cb5",
                                   "PT4041a3d8f8ac2849cddd390b4595a4206b6b94314380f601",
                                   signalwire_space_url='bowl-test.signalwire.com')
    calls = callClient.calls.list(start_time_after=start,
                                  start_time_before=end)
    d = []
    for record in calls:
        d.append(
            (record.from_formatted, record.to_formatted, record.start_time, str(record.duration) + " seconds",
             record.status, record.sid, record.price,
             record.direction))

    # format dataframe
    df = pd.DataFrame(d, columns=('From', 'To', 'Date', 'Duration', 'Status', 'Call SID', 'Price', 'Direction'))
    df['Price'] = df['Price'].fillna(0)
    df['Price'] = df['Price'].astype(float).round(4)
    df['Price'] = df['Price'].map('${:,.4f}'.format)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date', ascending=False)

    def hover(hover_color="lightblue"):
        return dict(selector="tr:hover",
                    props=[("background-color", "%s" % hover_color)])

    def highlightEven(even_color="lightgrey"):
        return dict(selector="tr:nth-child(even)",
                    props=[("background-color", "%s" % even_color)])

    th_props = [('padding-top', '12px'),
                ('padding-bottom', '12px'),
                ('text-align', 'center'),
                ('background-color', '#add8e6'),
                ('border', 'solid black')
                ]

    tr_props = [('padding-top', '12px'),
                ('padding-bottom', '12px'),
                ('text-align', 'center'),
                ('border', 'solid black')
                ]

    td_props = [('padding-top', '12px'),
                ('padding-bottom', '12px'),
                ('text-align', 'center'),
                ('border', 'solid black')
                ]

    caption_props = [('caption-side', 'top'),
                     ("font-size", "200%"),
                     ("text-align", "center"),
                     ("font", "bold")
                     ]

    styles = [
        hover(),
        highlightEven(),
        dict(selector="caption", props=caption_props),
        dict(selector='', props=[("border-collapse", "collapse")]),
        dict(selector='tr', props=tr_props),
        dict(selector='td', props=td_props),
        dict(selector='th', props=th_props),

    ]
    html = (df.style
            .set_table_styles(styles)
            .hide_index()
            .set_caption("Call Reporting - Hover to Highlight a Record.")
            .render())

    return html


def analyzeCalls():
    callClient = signalwire_client("e8f48a64-d62b-4bd5-a8d6-b26824a19cb5",
                                   "PT4041a3d8f8ac2849cddd390b4595a4206b6b94314380f601",
                                   signalwire_space_url='bowl-test.signalwire.com')

    calls = callClient.calls.list()
    d = []
    for record in calls:
        d.append((record.start_time, record.duration, record.status, record.direction, record.sid))
    df = pd.DataFrame(d, columns=('Date', 'Duration', 'Status', 'Direction', 'Sid'))
    df['Date'] = pd.to_datetime(df['Date'])

    # Show call status distribution
    statusCounts = df['Status'].value_counts()
    statusCounts.plot(kind='pie', autopct='%1.1f%%')
    plt.title("Distribution of Call Statuses")
    plt.ylabel('')
    plt.savefig('TrafficDashboard/static/callstatusdist.jpg')
    plt.close()

    # Show call type distribution
    statusCounts = df['Direction'].value_counts()
    statusCounts.plot(kind='pie', autopct='%1.1f%%')
    plt.title("Distribution of Call Types")
    plt.ylabel('')
    plt.savefig('TrafficDashboard/static/calltypedist.jpg')
    plt.close()

    # insert chart for call duration avg per month
    grouped = df.groupby(df['Date'].dt.to_period('m')).mean()
    grouped.plot()
    plt.title('Average Call Duration by Month')
    plt.ylabel('Call Duration in Seconds')
    plt.xlabel('')
    plt.savefig('TrafficDashboard/static/avgduration.jpg')
    plt.close()

    # insert chart for summary of calls per month
    groupedC = df.groupby(df['Date'].dt.to_period('m')).count()
    groupedC.plot(kind="barh", y='Sid', legend=False)
    plt.title('Number of Calls per Month')
    plt.xlabel('Number of Calls')
    plt.ylabel('')
    plt.savefig('TrafficDashboard/static/sumCalls.jpg')
    plt.close()


def analyzeMessages():
    messageClient = signalwire_client("0ea23c2c-6b11-4154-b3f3-49bd702936dd",
                                      "PT73051c323c68732cd9a0b1480b920d612b4c3bda3ca800c7",
                                      signalwire_space_url='bowl-test.signalwire.com')
    messages = messageClient.messages.list()
    d = []
    for record in messages:
        d.append((record.date_sent, record.status, record.direction, record.error_message))
    df = pd.DataFrame(d, columns=('Date', 'Status', 'Direction', 'Error'))
    df['Date'] = pd.to_datetime(df['Date'])

    # second array for containing status only
    m = []
    for record in messages:
        m.append(record.status)

    # Show message status distribution
    statusCounts = df['Status'].value_counts()
    statusCounts.plot(kind='pie', autopct='%1.1f%%')
    plt.title("Distribution of Message Statuses")
    plt.ylabel('')
    plt.savefig('TrafficDashboard/static/messagestatusdist.jpg')
    plt.close()

    # show message status distribution among OUTBOUND messages only
    # Transfer Variables to Int
    num_sent = int(m.count("sent"))
    num_received = int(m.count("received"))
    num_delivered = int(m.count("delivered"))
    num_undelivered = int(m.count("undelivered"))
    # Calculate Total Number Outbound Messages
    num_outbound_messages = num_sent + num_delivered + num_undelivered
    num_inbound_messages = num_received
    # Inbound vs Outbound Messages Pie Chart
    inbound_outbound = [num_inbound_messages, num_outbound_messages]
    my_colors = ['blue', 'grey']
    vs_label = ['Inbound', 'Outbound']
    plt.pie(inbound_outbound, colors=my_colors, autopct='%1.1f%%', labels=vs_label)
    plt.title('Inbound vs Outbound Messages')
    plt.savefig('TrafficDashboard/static/direction.jpg')
    plt.close()

    # Outbound Message Status Distribution
    outbound_pie_int = [num_sent, num_undelivered, num_delivered]
    outbound_pie_label = ['Sent', 'Undelivered', 'Delivered']
    my_colors2 = ['lightblue', 'Red', 'lightgreen']
    plt.pie(outbound_pie_int, labels=outbound_pie_label, autopct='%1.1f%%', colors=my_colors2)
    plt.title('Status of Outbound Messages')
    plt.savefig('TrafficDashboard/static/outstatusdist.jpg')
    plt.close()

    # Show message type distribution
    typeCounts = df['Direction'].value_counts()
    typeCounts.plot(kind='pie', autopct='%1.1f%%')
    plt.title("Distribution of Message Type")
    plt.ylabel('')
    plt.savefig('TrafficDashboard/static/messagetypedist.jpg')
    plt.close()

    # show number of messages per month
    groupedC = df.groupby(df['Date'].dt.to_period('m')).count()
    groupedC.plot(kind="barh", y='Status', legend=False)
    plt.title('Number of Messages per Month')
    plt.xlabel("Message Count")
    plt.ylabel('')
    plt.savefig("TrafficDashboard/static/messagesByMonth.jpg")

    # show error distribution
    errorCounts = df['Error'].value_counts()
    my_circle = plt.Circle((0, 0), 0.7, color='white')
    p = plt.gcf()
    p.gca().add_artist(my_circle)
    labels = ['"From" Number is Required to Send a Message', 'Trial Mode - "To" Number Not Verified', 'Unknown Error',
              'Unable to Deliver Message to Carrier', 'Unreachable Destination Handset', 'HTTP Retrieval Timeout',
              'Document Parse Error', 'HTTP Retrieval Failure']

    plt.figure(figsize=(8, 8))
    errorCounts.plot(kind='pie', autopct='%1.1f%%', startangle=90, labels=None)
    plt.legend(labels=labels, loc='lower left')
    plt.title("Distribution of Error Messages")
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('TrafficDashboard/static/errordist.jpg', edgecolor='w', pad_inches=.1)
    plt.close()


def analyzeBilling():
    # call client
    callClient = signalwire_client("e8f48a64-d62b-4bd5-a8d6-b26824a19cb5",
                                   "PT4041a3d8f8ac2849cddd390b4595a4206b6b94314380f601",
                                   signalwire_space_url='bowl-test.signalwire.com')

    messageClient = signalwire_client("0ea23c2c-6b11-4154-b3f3-49bd702936dd",
                                      "PT73051c323c68732cd9a0b1480b920d612b4c3bda3ca800c7",
                                      signalwire_space_url='bowl-test.signalwire.com')
    calls = callClient.calls.list()
    messages = messageClient.messages.list()
    d = []

    for record in calls:
        d.append(
            (record.start_time, record.price, record.direction + " call"))

    for record in messages:
        d.append((record.date_sent, record.price, record.direction + " message"))

    # format dataframe
    df = pd.DataFrame(d, columns=('Date', 'Price', 'Type'))
    df['Price'] = df['Price'].fillna(0)
    df['Price'] = df['Price'].astype(float).round(4)

    df = df.sort_values(by='Date', ascending=False)

    # average price spent per month line graph
    grouped = df.groupby(df['Date'].dt.to_period('m')).mean()
    grouped.plot()
    plt.title('Average Spend per Month')
    plt.xlabel('')
    plt.savefig('TrafficDashboard/static/avgspend.jpg')

    # total price spent per month
    grouped1 = df.groupby(df['Date'].dt.to_period('m')).sum()
    grouped1.plot(kind="barh")
    plt.title('Total Spend per Month')
    plt.ylabel('')
    plt.savefig('TrafficDashboard/static/sumspend.jpg')

    # show prices grouped by type bar chart
    type = []
    for record in calls:
        type.append(
            (record.price, record.direction + ' call'))
    for record in messages:
        type.append((record.price, record.direction + ' message'))

    tf = pd.DataFrame(type, columns=('Price', 'Type'))

    tf.Price = tf.Price.astype(float)
    tf['Price'] = tf['Price'].fillna(0)
    groupedType = tf.groupby(tf['Type']).sum()
    groupedType.plot(kind='barh')
    plt.title('Total Spend by Each Type')
    plt.tight_layout()
    plt.savefig('TrafficDashboard/static/pricebytype.jpg')

    groupedType.plot(kind='pie', autopct='%1.1f%%', subplots=True, legend=False, ylabel='')
    plt.title('Percent of Total Spend by Each Type ')
    plt.savefig('TrafficDashboard/static/percentspend.jpg', bbox_inches='tight')


@app.route("/home")
def home():
    return render_template('index.html', logo='/static/translogo.png')


@app.route("/displayAll")
def listAllComm():
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    return render_template('records.html', logo='/static/translogo.png', table=listAll(startDate, endDate))


@app.route("/displayMessages")
def listSomeMessages():
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    return render_template('records.html', logo='/static/translogo.png', table=listMessages(startDate, endDate))


@app.route("/displayCalls")
def listSomeCalls():
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    return render_template('records.html', logo='/static/translogo.png', table=listCalls(startDate, endDate))


@app.route("/displayCallAnalytics")
def callAnalytics():
    # create hard statistics here
    callClient = signalwire_client("e8f48a64-d62b-4bd5-a8d6-b26824a19cb5",
                                   "PT4041a3d8f8ac2849cddd390b4595a4206b6b94314380f601",
                                   signalwire_space_url='bowl-test.signalwire.com')
    calls = callClient.calls.list()
    d = []
    for record in calls:
        d.append(
            (record.start_time, record.duration,
             record.status, record.price,
             record.direction))

    df = pd.DataFrame(d, columns=('Date', 'Duration', 'Status', 'Price', 'Direction'))

    # get total calls on account
    totalCalls = len(df.index)

    # get total numbers on account
    incoming_phone_numbers = callClient.incoming_phone_numbers.list()
    n = []
    for record in incoming_phone_numbers:
        n.append(record.phone_number)
    totalNum = len(n)

    # overall cost spent on calls
    df.Price = df.Price.astype(float)
    df['Price'] = df['Price'].fillna(0)
    df['Sum'] = df['Price'].sum(skipna=True)
    df['Sum'] = df['Sum'].astype(float).round(4)
    df['Sum'] = df['Sum'].map('${:,.4f}'.format)
    priceSum = df['Sum'][1]

    df['DurationSum'] = df['Duration'].sum()
    durSum = df['DurationSum'][1]
    durSum = durSum / 60
    durSum = '{:,.2f}'.format(durSum)

    x = []
    for record in calls:
        x.append((record.from_formatted, record.duration))
    xf = pd.DataFrame(x, columns=('From', 'Duration'))

    # set some styling for tables
    dth_props = [
        ('padding-left', '12px'),
        ('padding-right', '12px'),
        ('text-align', 'center'),
        ('background-color', '#add8e6'),
        ('border', 'solid black')
    ]

    dtr_props = [
        ('padding-left', '12px'),
        ('padding-right', '12px'),
        ('text-align', 'center'),
        ('border', 'solid black')
    ]

    dtd_props = [
        ('padding-left', '12px'),
        ('padding-right', '12px'),
        ('text-align', 'center'),
        ('border', 'solid black')
    ]

    th_props = [
        ('text-align', 'center'),
        ('background-color', '#add8e6'),
        ('border', 'solid black')
    ]

    tr_props = [
        ('text-align', 'center'),
        ('border', 'solid black')
    ]

    td_props = [
        ('text-align', 'center'),
        ('border', 'solid black')
    ]

    dstyles = [
        dict(selector='', props=[("border-collapse", "collapse")]),
        dict(selector='tr', props=dtr_props),
        dict(selector='td', props=dtd_props),
        dict(selector='th', props=dth_props),

    ]
    styles = [
        dict(selector='', props=[("border-collapse", "collapse")]),
        dict(selector='tr', props=tr_props),
        dict(selector='td', props=td_props),
        dict(selector='th', props=th_props),

    ]

    # show number of calls per from number
    groupedCount = xf.groupby(xf['From']).count()
    groupedCount.columns = ['# of Calls']

    # show average call duration for each phone number
    groupedAvg = xf.groupby(xf['From']).mean()
    groupedAvg.columns = ['Duration in Seconds']

    table = (groupedCount.style
             .set_table_styles(styles)
             .render())

    table1 = (groupedAvg.style
              .set_table_styles(dstyles)
              .render())

    return render_template('callAnalytics.html', logo='/static/translogo.png', status='/static/callstatusdist.jpg',
                           type='/static/calltypedist.jpg', CallTotal=totalCalls, NumTotal=totalNum, Price=priceSum,
                           duration='/static/avgduration.jpg', summary='/static/sumCalls.jpg', durationS=durSum,
                           table=table, table1=table1, spendtype='/static/pricebytype.jpg')


@app.route("/displayMessageAnalytics")
def MessageAnalytics():
    # create hard statistics here
    messageClient = signalwire_client("0ea23c2c-6b11-4154-b3f3-49bd702936dd",
                                      "PT73051c323c68732cd9a0b1480b920d612b4c3bda3ca800c7",
                                      signalwire_space_url='bowl-test.signalwire.com')
    messages = messageClient.messages.list()
    d = []
    for record in messages:
        d.append((record.date_sent, record.status, record.direction, record.price))
    df = pd.DataFrame(d, columns=('Date', 'Status', 'Direction', 'Price'))
    df['Date'] = pd.to_datetime(df['Date'])

    # get total messages on account
    totalMess = len(df.index)
    print(totalMess)

    # get total numbers on account
    incoming_phone_numbers = messageClient.incoming_phone_numbers.list()
    n = []
    for record in incoming_phone_numbers:
        n.append(record.phone_number)
    totalNum = len(n)
    print(totalNum)

    # overall cost spent on messages
    df.Price = df.Price.astype(float)
    df['Price'] = df['Price'].fillna(0)
    df['Sum'] = df['Price'].sum(skipna=True)
    df['Sum'] = df['Sum'].astype(float).round(4)
    df['Sum'] = df['Sum'].map('${:,.4f}'.format)
    priceSum = df['Sum'][1]

    return render_template('messageAnalytics.html', logo='/static/translogo.png', status='/static/messagestatusdist.jpg',
                           type='/static/messagetypedist.jpg', totalMess=totalMess, totalNum=totalNum, price=priceSum,
                           error='/static/errordist.jpg', message='/static/messagesByMonth.jpg',
                           inbound='/static/direction.jpg',
                           outbound='/static/outstatusdist.jpg')


@app.route("/displayBillingAnalytics")
def BillingAnalytics():
    # create hard statistics here
    # overall cost spent on calls
    callClient = signalwire_client("e8f48a64-d62b-4bd5-a8d6-b26824a19cb5",
                                   "PT4041a3d8f8ac2849cddd390b4595a4206b6b94314380f601",
                                   signalwire_space_url='bowl-test.signalwire.com')
    calls = callClient.calls.list()
    c = []
    for record in calls:
        c.append(
            (record.start_time, record.price))

    df = pd.DataFrame(c, columns=('Date', 'Price'))

    df.Price = df.Price.astype(float)
    df['Price'] = df['Price'].fillna(0)
    df['Sum'] = df['Price'].sum(skipna=True)
    df['Sum'] = df['Sum'].astype(float).round(4)
    unfCSum = df['Sum'][1]
    df['Sum'] = df['Sum'].map('${:,.4f}'.format)
    callPriceSum = df['Sum'][1]

    # overall cost spent on messages
    messageClient = signalwire_client("0ea23c2c-6b11-4154-b3f3-49bd702936dd",
                                      "PT73051c323c68732cd9a0b1480b920d612b4c3bda3ca800c7",
                                      signalwire_space_url='bowl-test.signalwire.com')

    messages = messageClient.messages.list()
    m = []

    for record in messages:
        m.append((record.date_sent, record.price))

    mf = pd.DataFrame(m, columns=('Date', 'Price'))

    # overall cost spent on messages
    mf.Price = mf.Price.astype(float)
    mf['Price'] = mf['Price'].fillna(0)
    mf['Sum'] = mf['Price'].sum(skipna=True)
    mf['Sum'] = mf['Sum'].astype(float).round(4)
    unfMSum = mf['Sum'][1]
    mf['Sum'] = mf['Sum'].map('${:,.4f}'.format)
    messagePriceSum = mf['Sum'][1]

    # total cost of all spend
    totalSum = '${:,.4f}'.format(unfMSum + unfCSum)

    # Monthly cost on numbers
    incoming_phone_numbersM = messageClient.incoming_phone_numbers.list()
    incoming_phone_numbersC = callClient.incoming_phone_numbers.list()
    n = []
    for record in incoming_phone_numbersM:
        n.append(record.phone_number)
    for record in incoming_phone_numbersC:
        n.append(record.phone_number)

    totalNum = len(n)
    numCost = '${:.2f}'.format(totalNum * .20)

    # if we had a billing API, I assume we'd be able to query things like account balance, but I'll hardcode it for now
    balance = 401.84

    # set some styling for tables
    th_props = [
        ('padding-left', '20px'),
        ('padding-right', '20px'),
        ('padding-bottom', '6px'),
        ('text-align', 'center'),
        ('background-color', '#add8e6'),
        ('border', 'solid black')
    ]

    tr_props = [
        ('padding-left', '20px'),
        ('padding-right', '20px'),
        ('padding-bottom', '6px'),
        ('text-align', 'center'),
        ('border', 'solid black')
    ]

    td_props = [
        ('padding-left', '20px'),
        ('padding-right', '20px'),
        ('padding-bottom', '6px'),
        ('text-align', 'center'),
        ('border', 'solid black')
    ]

    styles = [
        dict(selector='', props=[("border-collapse", "collapse")]),
        dict(selector='tr', props=tr_props),
        dict(selector='td', props=td_props),
        dict(selector='th', props=th_props),

    ]

    # show prices grouped by month
    month = []
    for record in calls:
        month.append(
            (record.price, record.start_time, record.direction + ' call'))
    for record in messages:
        month.append((record.price, record.date_sent, record.direction + ' message'))

    mof = pd.DataFrame(month, columns=('Price', 'Date', 'Type'))
    mof.Price = mof.Price.astype(float)
    mof['Price'] = mof['Price'].fillna(0)

    # show avg spend each month
    groupedAvgSpend = mof.groupby(mof['Date'].dt.to_period('m')).mean()
    table1 = (groupedAvgSpend.style
              .set_table_styles(styles)
              .render())

    # show total spend each month
    groupedSumSpend = mof.groupby(mof['Date'].dt.to_period('m')).sum()
    table2 = (groupedSumSpend.style
              .set_table_styles(styles)
              .render())

    return render_template('billingAnalytics.html', image='/static/swlogo.jpg', sum='/static/sumspend.jpg',
                           avg='/static/avgspend.jpg', NumTotal=numCost, MessageTotal=messagePriceSum,
                           CallTotal=callPriceSum, TotalCost=totalSum, spendtype='/static/pricebytype.jpg',
                           balance=balance, table1=table1, table2=table2, percentspend='/static/percentspend.jpg')


if __name__ == "__main__":
    app.run(debug=True)

