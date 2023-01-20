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
## Documentation
### [SMTP Library](https://docs.python.org/3/library/smtplib.html)
- Used to setup secure connection to Google's SMTP Server and send the message
### [Gmail App Password](https://support.google.com/accounts/answer/185833?hl=en)
- Required for access to the Gmail Account, I would reccomend creating a burner account so anything important is not compromised if something goes wrong or the password is somehow leaked.
- You will need to setup 2-Factor Verification to access App Passwords
### [Colorama](https://pypi.org/project/colorama/)
- For coloring diagnostic text (NOT REQUIRED FOR PROGRAM TO RUN)
### [Datetime](https://docs.python.org/3/library/datetime.html)
- For diagnostics (NOT REQUIRED FOR PROGRAM TO RUN)
## Functions
### send(phone_number, carrier, message):
- Handles the server connection, Gmail connection and message sending
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
# USING Python_SMS(sendSMS.py)
- Assuming your Gmail and App Password are Valid
- Assuming the phone number and carrier are valid
### main.py
```python
import SMS

recipient_phone_number = '1234567890'

recipient_carrier = 'Verizon'

message_to_send = 'Test Message from sendSMS.py'

SMS.send(recipient_phone_number, recipient_carrier, message_to_send)
```
### Console Output:
```
1234567890 is valid
Verizon is valid
Login Successful
Send Successful

check phone in a few seconds and the message should be there
```
# Feedback is appreciated if you have ideas to improve this!
