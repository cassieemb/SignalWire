from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os

scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(os.getcwd() + "/creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Lost_Package_Requests").sheet1