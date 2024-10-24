# Author: https://github.com/Namelocms
# Last updated: 10/23/2024
# GitHub Repository: https://github.com/Namelocms/Squid_SMS
# Copyright (c) 2024 Sean Coleman

import smtplib as smt
import logging as log

class SquidSMS:
    def __init__(self, email, password):
        # Cellular Service Providers
        self.CARRIERS = {
            'att': '@mms.att.net',
            'Att': '@mms.att.net',
            'ATT': '@mms.att.net',

            'tmobile': '@tmomail.net',
            'Tmobile': '@tmomail.net',
            'TMobile': '@tmomail.net',
            'TMOBILE': '@tmomail.net',

            'verizon': '@vtext.com',
            'Verizon': '@vtext.com',
            'VERIZON': '@vtext.com',

            'sprint': '@page.nextel.com',
            'Sprint': '@page.nextel.com',
            'SPRINT': '@page.nextel.com'
        }

        # Email to use in sending the SMS
        self.AUTH_EMAIL = email

        # App Password (not email password) for 'AUTH_EMAIL'
        self.AUTH_PASS = password

        # Email + Password used to send message
        self.auth = (self.AUTH_EMAIL, self.AUTH_PASS)

    # Connect to the SMTP server
    def connect(self):
        try:
            # Establish a secure session with gmail's outgoing SMTP server using your gmail account
            server = smt.SMTP("smtp.gmail.com", 587)
            server.starttls()
            if server.login(self.auth[0], self.auth[1]):
                return server
            else:
                raise smt.SMTPAuthenticationError
        except smt.SMTPAuthenticationError:
            log.error('Error connecting to the server (check credentials)')
            return server.quit()  # end server connection


    def send(self, server, phone_number, carrier, message):
        # server is returned as type tuple() on disconnect, so if not disconnected, continue
        if type(server) is tuple:
            log.error('Server is not connected, check email and app password')
            self.disconnect(server=server)
            return False
        if self.check_phone_number(phone_number) and self.check_carrier(carrier):
            # convert phone_number and carrier into usable string
            recipient = "{} {}".format(phone_number, self.CARRIERS[carrier])
            # Send text message through SMS gateway of destination number
            try:
                server.sendmail(self.auth[0], recipient, message)
                return True
            except (smt.SMTPAuthenticationError, AttributeError):
                log.error('Send failed')
                self.disconnect(server=server)
                return False
        else:
            log.error('Issue with phone number or carrier')
            self.disconnect(server=server)
            return  False

    @staticmethod
    def disconnect(server):
        try:
            server.quit()
        except AttributeError:
            pass

    @staticmethod
    def check_phone_number(phone_number):
        if len(phone_number) != 10:
            log.error('Phone number length not 10')
            return False
        try:
            int(phone_number) # is number?
            return True
        except ValueError:
            log.error('Phone number contains non-numerical character(s)')
            return False

    def check_carrier(self, carrier):
            if carrier in self.CARRIERS:
                return True
            log.error('Carrier does not exist')
            return False
