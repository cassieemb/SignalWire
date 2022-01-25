# **Full Service SMS App**

## To Do Next: 
* set up number group page
* allow messaging to send from number groups 
* make message history show past 24 hours by default 
* how to accept additional filters, maybe use optional parameters and check if they exist?
* set up fetch function for additional message filters, will implement in history/errors on browser


### Bulk messaging 
 * **Choose from available customer CSVs, set template, and send out messaging**
* send from available number group

### Set up number groups 
* allow to show all numbers on account 
* allow to choose numbers and add to number group 
* show groups with name, associated numbers, sid 
    

### Upload Customer Lists
* **change all numbers to have + prefix**
* **check for previously opted out people and alert to remove**
* **allow for retries if input is invalid** 

  
### Delete Customer Records 
* **delete based on absolute path (used when opted out customer is uploaded)**
* **delete based on src/ folder (used when customer opts out)**

### **Private Shortened URLs**
* **encode full URLs into shortened URLs and store as key/value pair in dict**
* **decode shortened URLs and redirect to full URL**

### Message History Section 
* **by default show all results** 
* allow for additional filtering on browser
* set up to refresh every 2 minutes
* click sid to view additional details (use fetch function)
    
    
### Utilize status callbacks to keep track of errors
* do something if error rate gets too high
* click sid to view additional details (use fetch function)
    

### Manage opt outs 
* **monitor inbound messages for stop phrase**
* **remove people who opt out from subscriber lists**
* **add them to do not contact lists**
* monitor opt out rate, do something if opt out rate gets too high
  

### Conversational messaging