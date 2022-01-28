# **Full Service SMS App**

## To Do Next:
* finish file upload - call upload function from flask and reload page 
* current issue - file upload doesn't pass actual file through url in upload file parameter 

  

* Work on Message History and Error Center front end
* translate phone numbers with - to e164

-------

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
* add reload page 
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