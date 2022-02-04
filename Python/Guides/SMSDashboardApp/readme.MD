# **Full Service SMS App**
## Currently Working on:
### Error history Page 
- remove all entries more than 48 hours before current time
- click sid for additional details in pop up box 

## Come back to:
### Error history Page 
- set all phone numbers on project to hostname/inbound webhook 

### Message history 
* fix sidebar without changing background
* add progress bar
* fixed header while scrolling
* click sid for additional details in pop up box 

### Bulk messaging section
- progress bar
- twilio.base.exceptions.TwilioRestException: HTTP 422 error: Unable to create record: Messagingservicesid does not have a SMS-capable phone number in the group.
- Show all sends in table (date of send, customer data file used, total number of messages sent, success rate? )
- set status callback URL in message send

### Customer Data Page
* current issue - file upload doesn't pass the actual file through url in upload file parameter
* set up alert for when customer has already opted out