# **Full Service SMS App**

## WorkList
- don't allow submit if body is empty or radio boxes not selected
- radio button is sending 'on' even when off
- only send the selected element 

### Bulk messaging section
- add an alert when bulk send is done with amount of messages sent and time elapsed

### Error history Page 
- remove all entries more than 48 hours before current time 
- figure out if worth offering additional filters instead of live stream only 

### Message history 
* fix sidebar without changing background
* add progress bar
* fixed header while scrolling

### Customer Data Page
* current issue - file upload doesn't pass actual file through url in upload file parameter

### Number Groups Section 
- fix styling of page - change top to toggle where correct div only shows when toggled?
- refresh page at number group if new group is created
- refresh page at number group if numbers are added to group 
- change h3 to change if group is empty or if none is selected 

### Home page 
- font is weird 
- make icons clickable
- make everything look cleaner and adjust color palettes
  

## Core pieces of application

### Bulk Messaging Section
* **Choose from available customer CSVs, set template, and send out messaging**
* **send from number group**
* show all numbers on account and choose from number

-------

### Number Groups Section 
* **allow to show all numbers on account**
* **display all number groups, display all number group members**
* **add a number to a number group** 
-------

### Customer Data Section
#### Upload Customer Lists
* **change all numbers to have + prefix**
* **check for previously opted out people and alert to remove**
* **allow for retries if input is invalid**
  
#### Delete Customer Records 
* **delete based on absolute path (used when opted out customer is uploaded)**
* **delete based on src/ folder (used when customer opts out)**
-------

### **Private Shortened URLs Section**
* **encode full URLs into shortened URLs and store as key/value pair in dict**
* **decode shortened URLs and redirect to full URL**

-------

### Message History Section 
* **by default show all results between yesterday and present time** 
* **allow for additional filtering when specified**
* click sid to view additional details (use fetch function)
    
-------    
### Error Reporting Section
* utilize status callbacks to show error history since app was loaded 
* click sid to view additional details (use fetch function)

-------

### Opt Out Manager
* **monitor inbound messages for stop phrase**
* **remove people who opt out from subscriber lists**
* **add them to do not contact lists**

-------

### Wish List: Maybes?
* keep track of errors per 24 hour period 
* keep track of opt outs per 24 hour period 
* create alert function that texts? emails? admin if opt out rate or error rate is too high 
* Conversational messaging