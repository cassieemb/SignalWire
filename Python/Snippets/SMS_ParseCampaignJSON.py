import requests

url = "https://example.signalwire.com/api/relay/rest/registry/beta/campaigns/YourIDHere/numbers"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "Basic ZjRjNzg4ZDItODQzYi00ZDA1LTk1ZTgtNDc1YjYyYWU2YzU4OlBUYWFhZGE2Yjc2ZjRhZTA0MDA3NGZjMzQ4OTAwY2NiM2I3YTYyY2NjNDI5NTFlMWE3"
}

response = requests.request("GET", url, headers=headers)

jsonString = response.json()
print("Json String is: ")
print(jsonString)

phone_number = jsonString['data'][0]['phone_number']['number']
print(phone_number)

