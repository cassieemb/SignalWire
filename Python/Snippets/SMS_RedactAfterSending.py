from signalwire.rest import Client as signalwire_client
import time

client = signalwire_client("ProjectID", "AuthToken", signalwire_space_url = 'SpaceURL.signalwire.com')

phone_number_list = ['+12147903161', '+13463681679']

for x in phone_number_list:
    message = client.messages.create(
                                from_='+19043445583',
                                body="We're going to redact this for Hippa",
                                to=x
                            )

    # sleep for a period of time to account for while the message sending is in progress
    time.sleep(60)

    # use this to update the message body but keep the message record
    messages = client.messages(message.sid) \
                    .update(body='')
    print("Message Redacted")

    # uncomment this line and comment the above one if instead you want to FULLY delete the message, erasing all message history
    #client.messages(message.sid).delete()