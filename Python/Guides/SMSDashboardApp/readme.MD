# **Full Service SMS App**

## To Do Next:
* accept additional parameters optionally in message history, apply button will implement them 
* keep track of errors per 24 hour period 
* keep track of opt outs per 24 hour period 
* create alert function that texts? emails? admin if opt out rate or error rate is too high 


### Bulk messaging 
 * **Choose from available customer CSVs, set template, and send out messaging**
* **send from number group**

### Set up number groups 
* **allow to show all numbers on account**
* **display all number groups, display all number group members**
* **add a number to a number group** 
    

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
* **by default show all results between yesterday and present time** 
* allow for additional filtering on browser
* set up to refresh every 2 minutes
* click sid to view additional details (use fetch function)
    
    
### Utilize status callbacks to keep track of errors
* do something if error rate gets too high
* click sid to view additional details (use fetch function)
    
### Fetch Additional Details 
* In status callback and message history section, allow click on sid to call function 
  and return additional information about the message via alert box 
  
### Manage opt outs 
* **monitor inbound messages for stop phrase**
* **remove people who opt out from subscriber lists**
* **add them to do not contact lists**
* monitor opt out rate, do something if opt out rate gets too high
  

### Conversational messaging