# Python_SMS
## WARNING, CONSENT IS KEY ;)
DO NOT USE THIS TO PERFORM ILLEGAL ACTIVITIES SUCH AS:
- MASS TEXTING
- COLD TEXTING
- AND EVERYTHING ELSE
- refer to https://www.fcc.gov/tags/telephone-consumer-protection-act-tcpa for more information
### Standard Message and Data Rates Apply
## Purpose
Sends an SMS message to a desired phone number using your Gmail Account, great for sending yourself info quick for reminders, etc.
## Drawbacks
- Cannot check if message was received,
- Cannot check if phone number is real,
- Cannot receive messages from recipient phone number
- [Message sends limited by gmail](https://support.google.com/a/answer/2956491#sendinglimitsforrelay&zippy=%2Creview-sending-limits-for-the-smtp-relay-service)
- Sending with .format() leads to unintended message contents:
  ```python
  client_name = 'Bob'
  
  message = 'Hi {}, you're awesome!'.format(client_name)
  
  # Intended message: Hi Bob, you're awesome!
  
  # Actual message: Hi Bob, you're awesome!
  #                 X-CMAE-Envelope:
  #                 MWi19ow8hdinjasdiuioais
  #                 mOIaundaoiudnaoinsdao1/
  #                 W<M)D_!JI_!_JIDNU#I#KAJ
  
  ```
## Documentation
### [SMTP Library](https://docs.python.org/3/library/smtplib.html)
- Used to setup secure connection to Google's SMTP Server and send the message
- [Some possible Error Codes](https://www.arclab.com/en/kb/email/smtp-response-codes-error-messages.html#:~:text=SMTP%20Error%20221&text=Error%20221%20is%20an%20authentication,and%20user%2Fpassword%20is%20correct.)
### [Gmail App Password](https://support.google.com/accounts/answer/185833?hl=en)
- Required for access to the Gmail Account, I would reccomend creating a burner account so anything important is not compromised if something goes wrong or the password is somehow leaked.
- You will need to setup 2-Factor Verification to access App Passwords
### [Colorama](https://pypi.org/project/colorama/)
- For coloring diagnostic text (NOT REQUIRED FOR PROGRAM TO RUN)
### [Datetime](https://docs.python.org/3/library/datetime.html)
- For diagnostics (NOT REQUIRED FOR PROGRAM TO RUN)
## Functions
### connect():
- Handles SMTP Server connection, Gmail Login
- returns server object if successful
- returns tuple with disconnect code at index 0 if failure (code 221 is normal for this style disconnect)
### send(phone_number, carrier, message):
- Handles the message sending
- all three parameters should be strings
  - phone_number: no spaces or non-number characters
  - carrier: must match one in the dictionary
  - message: anything in string form
- returns bool
### check_phone_number(phone_number):
- Ensures phone_number formatting is correct
- returns bool
### check_carrier(carrier):
- Ensures carrier is valid
- returns bool
### disconnect(server):
- Handles disconnection from SMTP Server
- returns nothing
## Constants
### AUTH_EMAIL (string):
- The email address you want to use in sending the SMS
- Ex: 'myemail@gmail.com'
### AUTH_PASS (string):
- App Password provided by Gmail (wont work if you use the Gmail password generally used to sign-in), this should be a 16-Character string
- Ex: 'oiu12dmi12p9knao'
### CARRIERS (string-Dictionary):
- Holds Email-SMS conversion addresses for each provider
- Really only need one for each, but i provided different case usage for variability sake
# Example using PythonSMS
- Assuming your Gmail and App Password are Valid
- Assuming the phone number and carrier are valid
### main.py
```python
from SMS import SendSMS

initializeClass = SendSMS('your_gmail', 'your_app_password')

# Connect to SMTP server and store it
server = test.connect()

# Parameters should all be strings
recipient_number = '1234567890'
recipient_carrier = 'Verizon'
my_message = 'Wow this is pretty cool!'

# If the send is successful, call function to disconnect from server
result = initializeClass.send(server, recipient_number, recipient_carrier, my_message)
if result:
    initializeClass.disconnect(server)
```
### Console Output:
```
1234567890 is valid
Verizon is valid
Login Successful
Send Successful
SMTP Server Connection Ended!

check phone in a few seconds and the message should be there
```
## Roadmap
### ☐ Implement custom GUI
### ☐ Add ability to recieve messages (if possible)
### ☐ Add ability to check message recieved by target number (if possible)
### ☐ Add ability to check number is in service before sending
# Feedback is appreciated!
