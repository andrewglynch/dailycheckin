# script executes the final part of the daily process
# and loops over the recipient_array to send the daily SMS messages
# from Twilio using the stored credentials


# set up packages
from decouple import config
from twilio.rest import Client
from pyairtable import Table
from datetime import datetime
import gspread


# import account credentials from .env file using config
twilio_account_SID = config('TWILIO_ACCOUNT_SID')
twilio_auth_token = config('TWILIO_AUTH_TOKEN')
airtable_API_key = config('AIRTABLE_API_KEY')
airtable_DCI_base_ID = config('AIRTABLE_DCI_BASE_ID')
gc =gspread.service_account(filename='credentials.json')


# Authenticate Twilio and set send number
client = Client(twilio_account_SID, twilio_auth_token)
twilio_send_number = "+18149294918"


# grab data from Airtable
table_ID = 'tbloak1BYkenVSFGP'
table = Table(airtable_API_key, airtable_DCI_base_ID, table_ID)
airtable_export = table.all()


# Establish empty array to add recipient phone numbers to
recipient_list = []


# set correct google sheet as variable and select body of SMS from cell
sh = gc.open_by_key('1i-dzPtKYxAnQVjWCMS3IeFVr3bruh9XUAPgKKQlp6i4')
text_body = sh.worksheet('Text string').acell('B2').value
print(text_body)


# conditionals to ensure weekend texts only go to those who have opted in
# based on flows, appends recipient phone number to array
weekday_number = (datetime.today().weekday())
if weekday_number == 5 or weekday_number == 6:

    for records in airtable_export:
        if records['fields']['Subscription_status']=='Subscribed' and records['fields']['Weekend_texts']=='Yes':
            recipient_list.append(records['fields']['Phone number'])
        else:
            continue
else:
    for records in airtable_export:
        if records['fields']['Subscription_status']=='Subscribed':
            recipient_list.append(records['fields']['Phone number'])
        else:
            continue


print("This message will go to "+str(len(recipient_list))+" recipients. Starting now...")


# loop over array to send messages
for i in recipient_list:
    message = client.messages.create(
        body=text_body,
        from_=twilio_send_number,
        to=i)
    print("Message sent successfully to "+i+".")


print("All done for today!")
