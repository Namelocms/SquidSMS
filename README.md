# SquidSMS
SquidSMS is a Python-based SMS sending tool that allows you to send SMS messages using a Gmail account. It provides a convenient way to send quick reminders and information to yourself or other **consenting** parties. The tool is designed to be easy to use and provides functionality for connecting to the SMTP server, sending messages, validating phone numbers, and validating carriers.

## Disclaimer
- Please use this tool responsibly and in accordance with applicable laws and regulations. Do not use it for illegal activities.
Refer to **https://www.fcc.gov/tags/telephone-consumer-protection-act-tcpa** for more information.
- **Standard Message and Data Rates may apply**

## Table of Contents
- [Getting Started](#getting-started)
- [Documentation](#documentation)
- [Example](#example)
- [Drawbacks](#drawbacks)

## Getting Started
Before using SquidSMS, make sure you have the necessary dependencies:
- [SMTP Library](https://docs.python.org/3/library/smtplib.html) `smtplib` for establishing an SMTP connection.
  - ```bash
    pip install smtplib
  - [Some possible Error Codes](https://www.arclab.com/en/kb/email/smtp-response-codes-error-messages.html#:~:text=SMTP%20Error%20221&text=Error%20221%20is%20an%20authentication,and%20user%2Fpassword%20is%20correct.)
- [Colorama](https://pypi.org/project/colorama/) for colorful console output.
  - ```bash
    pip install colorama
- Python's [Datetime](https://docs.python.org/3/library/datetime.html) for diagnostics.
- [Gmail App Password](https://support.google.com/accounts/answer/185833?hl=en)
  - Required for access to the Gmail Account, I would reccomend creating a burner account so anything important is not compromised if something goes wrong or the password is somehow leaked.
  - You will need to setup 2-Factor Verification to access App Passwords through Google

## Documentation
### Class: SquidSMS
#### Methods
| Method                | Description                                                                             | Parameters                                     | Returns |
|-----------------------|-----------------------------------------------------------------------------------------|-------------------------------------------------|---------|
| `__init__`           | Initializes the SendSMS class, sets up the `CARRIERS` dictionary, and assigns the authentication values                            | `email` (string), `password` (string)                                            | None    |
| `connect()`           | Connects to the SMTP server using Gmail account credentials.                            | None                                            | Server object or tuple with disconnect code    |
| `send()`              | Sends an SMS message. Checks phone number and carrier validity.                         | `phone_number` (string), `carrier` (string), `message` (string) | Boolean (success status)                        |
| `check_phone_number()`| Checks if the provided phone number is correctly formatted (10-digit format).            | `phone_number` (string)                        | Boolean (validity)                              |
| `check_carrier()`     | Checks if the provided carrier is valid and supported.                                  | `carrier` (string)                             | Boolean (validity)                              |
| `disconnect()`        | Handles the disconnection from the SMTP server.                                        | `server` (object)                              | None    |
#### Constants
- CARRIERS (dictionary):
  - Defines cellular service providers and their email-to-SMS conversion addresses.
- AUTH_EMAIL (string): Your Gmail email address.
- AUTH_PASS (string): An App Password provided by Google Authentication. It should be a 16-character string.
#### Valid Numbers
- This will work with any number which follows the 10-digit format and is covered by one of the available carriers
  - To change the number format, edit the code in `check_number` to an number which applies to your situation.
- DO NOT include country codes in the phone numbers, through my testing with numbers from the USA, +1 country code, this will break the send process.
#### Carriers and Numbers
- When sending to a number, the number MUST be covered by the selected carrier. If there is a mismatch between carrier and number the message will send but wont be delivered.
- You can add new carriers to the program by modifying the `CARRIERS` dictionary with the new carrier name and email domain.
#### Email and Password
- EMAIL: This should be your GMAIL account that you want to use in sending the messages
- PASSWORD: The App password provided by Google Authentication, should be a 16-character string

## Example
**main.py:**
  ```python
  from SMS import SendSMS

  your_gmail = 'example@gmail.com'
  your_app_password = 'oiu12dmi12p9knao'

  # Initialize the class
  example = SendSMS(your_gmail, your_app_password)

  # Connect to SMTP server and store it
  server = example.connect()

  # Parameters should all be strings
  recipient_number = '8881237890'
  recipient_carrier = 'Verizon'
  my_message = 'Wow this is pretty cool!'

  # If the send is successful, call function to disconnect from server
  result = example.send(server, recipient_number, recipient_carrier, my_message)
  if result:
    example.disconnect(server)
  ```
**Console Output:**
```
1234567890 is valid
Verizon is valid
Login Successful
Send Successful
SMTP Server Connection Ended!

check phone in a few seconds and the message should be there
```
### How it Works
- The recipient's number will be prepended to the email domain address of the chosen carrier like this:
  - `number = '5551234567', carrier = '@mms.att.net', recipient = '5551234567@mms.att.net'`
- From there the SMTP server provided by Google is connected to, using your email and password, and the message is sent to the new recipient email address
- The message is then transmitted from that new email address to the device associated with the number.

## Drawbacks
- Cannot check if message was received,
- Cannot check if phone number is real,
- Cannot receive messages from recipient phone number
- [Message sends limited by gmail](https://support.google.com/a/answer/2956491#sendinglimitsforrelay&zippy=%2Creview-sending-limits-for-the-smtp-relay-service)
- Sending with .format() leads to unintended message contents:
  ```python
  client_name = 'Bob'
  
  message = 'Hi {}, you\'re awesome!'.format(client_name)
  
  # Intended message: Hi Bob, you're awesome!
  
  # Actual message: Hi Bob, you're awesome!
  #                 X-CMAE-Envelope:
  #                 MWi19ow8hdinjasdiuioais
  #                 mOIaundaoiudnaoinsdao1/
  #                 W<M)D_!JI_!_JIDNU#I#KAJ
  
  ```

**Copyright**: © 2023 Sean Coleman <br> **Last Updated**: 01/31/2023
