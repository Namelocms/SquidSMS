# Author: https://github.com/Namelocms
# Last updated: 04/13/2023
# GitHub Repository: https://github.com/Namelocms/Python_SMS


# No resize of window (must be first kivy import)
from kivy.config import Config
Config.set('graphics', 'resizable', False)

from kivy.app import App  # Run app
from kivy.lang import Builder  # Build settings
from kivy.uix.label import Label  # Text label
from kivy.core.window import Window  # Window configs
from kivy.uix.screenmanager import Screen, ScreenManager  # Change screens
from kivy.properties import ObjectProperty  # Variables
from kivy.uix.popup import Popup  # Warning popups

import webbrowser  # Hyperlinks
import json         # reading, writing files
import smtplib as smt  # Server connections

##########################################################################################
# Server Connection/Send Message Class
##########################################################################################
class SendSMS:
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
        server = None
        try:
            # Establish a secure session with gmail's outgoing SMTP server using your gmail account
            server = smt.SMTP("smtp.gmail.com", 587)
            server.starttls()

            if server.login(self.auth[0], self.auth[1]):
                return server

            else:
                raise smt.SMTPAuthenticationError

        except smt.SMTPAuthenticationError:
            return server.quit()  # end server connection, returns tuple()

    # Send the message
    def send(self, server, recipient, message, num_to_send):
        # server is returned as type tuple() on disconnect, so if not disconnected, continue
        if type(server) is not tuple:
            try:
                # Number sent
                x = 0

                while x < int(num_to_send):
                    x += 1
                    # Send text message through SMS gateway of destination number
                    server.sendmail(self.auth[0], recipient, message)

                self.disconnect(server)
                return True

            except (smt.SMTPAuthenticationError, AttributeError):
                # In case connection is ended already
                try:
                    self.disconnect(server)
                except AttributeError:
                    pass
                return False

        else:
            # In case connection is ended already
            try:
                self.disconnect(server)
            except AttributeError:
                pass
            return False

    # end server connection
    @staticmethod
    def disconnect(server):
        server.quit()  # end server connection

    # Ensure provided number formatting is correct,
    # wont check if number is real or not
    @staticmethod
    def check_phone_number(phone_number):
        if len(phone_number) == 10:
            try:
                int(phone_number)  # is number?
                return True
            except ValueError:
                return False
        else:
            return False

    # Check carrier is valid
    def check_carrier(self, carrier):
        if carrier in self.CARRIERS:
            return True
        return False

    # Check email
    @staticmethod
    def check_email(email):
        if '@gmail.com' in email:
            return True
        else:
            return False

    # check password, must be 16 characters since that is Google's App Password format
    @staticmethod
    def check_password(password):
        if len(password) != 16:
            return False
        else:
            return True


##########################################################################################
# Start GUI Classes
##########################################################################################

# Format: {'gmail': {'password': string, 'total': int}, ...}
accounts = {}

# Screen Changing
sm = ScreenManager()


class LoginScreen(Screen):
    gmail = ObjectProperty(None)
    app_pass = ObjectProperty(None)

    # Handle Login
    def login(self):
        g = self.gmail.text.strip().lower()
        a = self.app_pass.text.strip()

        # used to check format of gmail and password, cleared after use
        temp_auth = SendSMS(g, a)

        # Check formatting is correct
        if temp_auth.check_email(g) is False or temp_auth.check_password(a) is False:
            pop = Popup(title='Login Error',
                        size_hint=(None, None), size=(200, 100),
                        content=Label(text='Email or Password\n'
                                           '          Invalid',
                                      font_size=11))
            pop.open()
            temp_auth = None
            sm.current = 'login'

        else:
            try:
                account = accounts[g]
                if a == account['password']:
                    sm.current = 'send'
                else:
                    raise KeyError
            except KeyError:
                pop = Popup(title='Login Error',
                            size_hint=(None, None), size=(200, 100),
                            content=Label(text='Email or Password\n'
                                               '          Invalid',
                                          font_size=11))
                pop.open()
                temp_auth = None
                sm.current = 'login'

    # Check/add new Gmail and password
    def add_account(self):
        g = self.gmail.text.strip().lower()
        a = self.app_pass.text.strip()

        # used to check format of gmail and password, cleared after use
        temp_auth = SendSMS(g, a)

        if temp_auth.check_email(g) is False:
            pop = Popup(title='EMAIL ADDRESS INVALID',
                        size_hint=(None, None), size=(200, 100),
                        content=Label(text='MUST CONTAIN:\n'
                                           '   \'@gmail.com\'',
                                      font_size=11))
            pop.open()
            temp_auth = None
            sm.current = 'login'

        elif temp_auth.check_password(a) is False:
            pop = Popup(title='PASSWORD INVALID',
                        size_hint=(None, None), size=(200, 100),
                        content=Label(text='MUST CONTAIN:\n'
                                           '   \'16 Characters\'',
                                      font_size=11))
            pop.open()
            temp_auth = None
            sm.current = 'login'

        elif g in accounts:
            pop = Popup(title='Authentication Error',
                        size_hint=(None, None), size=(200, 100),
                        content=Label(text='Account Exists!\nLog in'))
            pop.open()
            temp_auth = None
            sm.current = 'login'

        else:
            accounts.update({g: {'password': a, 'total': 0}})
            temp_auth = None
            sm.current = 'send'

    @staticmethod
    def reset_send():
        sm.screens[1].mobile.text = ''
        sm.screens[1].carrier.text = ''
        sm.screens[1].message.text = ''
        sm.screens[1].number.text = '1'


class SendScreen(Screen):
    gmail = ObjectProperty(None)
    mobile = ObjectProperty(None)
    carrier = ObjectProperty(None)
    message = ObjectProperty(None)
    number = ObjectProperty(None)

    # Show Gmail address being used
    def on_enter(self, *args):
        self.gmail.text = sm.screens[0].gmail.text.strip()  # set gmail address label

    # Add 1 to number of messages
    def add_one(self):
        try:
            if int(self.number.text) >= 10:
                pass
            else:
                self.number.text = str(int(self.number.text) + 1)
        except ValueError:  # catch non-int input
            self.number.text = '1'

    # Subtract 1 from number of messages
    def sub_one(self):
        try:
            if int(self.number.text) <= 1:
                pass
            else:
                self.number.text = str(int(self.number.text) - 1)
        except ValueError:  # catch non-int input
            self.number.text = '1'


    # Make sure number of messages is valid

    def check_number(self):
        try:
            if self.number.text == '' or 1 > int(self.number.text) or int(self.number.text) > 10:
                return False
        except ValueError:  # catch non-int input
            return False
        return True

    # Check parameters then connect to server and send message
    def send_message(self):
        # Access Login Screen gmail/app-password value
        gmail = sm.screens[0].gmail.text.strip()
        app_pass = sm.screens[0].app_pass.text.strip()

        # initialize recipient
        recipient = ''

        # initialize SendSMS class
        key = SendSMS(gmail, app_pass)

        # check message amount
        if self.check_number() is False:
            pop = self.pop_number()
            pop.open()
            sm.current = 'send'

        # check carrier
        if key.check_carrier(self.carrier.text) is True and key.check_phone_number(self.mobile.text) is True:
            # convert phone_number and carrier into usable string
            recipient = "{} {}".format(self.mobile.text, key.CARRIERS[self.carrier.text])

        else:
            pop = self.pop_mobile_carrier()
            pop.open()
            sm.current = 'send'

        # server is returned as type tuple() on disconnection
        server = key.connect()
        if type(server) is tuple:
            pop = self.pop_server(server)
            pop.open()
            sm.current = 'send'

        # If everything was successful, move to the confirmed page
        else:
            if recipient != '':
                if key.send(server, recipient, self.message.text, self.number.text):
                    sm.current = 'confirmed'
                else:
                    sm.current = 'send'
            else:
                sm.current = 'send'
    
    @staticmethod
    def pop_number():
        pop = Popup(title='Message Amount Invalid',
                    size_hint=(None, None), size=(200, 100),
                    content=Label(text='ONLY 1-10 MESSAGES CAN\n'
                                       'BE SENT AT A TIME',
                                  font_size=11))
        return pop

    @staticmethod
    def pop_mobile_carrier():
        pop = Popup(title='  INVALID PARAMETER',
                    size_hint=(None, None), size=(200, 100),
                    content=Label(text='CHECK NUMBER IS VALID\n'
                                       '                    or\n'
                                       '   CHECK CARRIER VALID',
                                  font_size=11))
        return pop

    @staticmethod
    def pop_server(server_code):
        pop = Popup(title='Server Connection Failed:: Code: {}'.format(server_code[0]),
                    size_hint=(None, None), size=(265, 100),
                    content=Label(text='CHECK GMAIL / PASSWORD\n'
                                       '                    or\n'
                                       '       CHECK HELP PAGE',
                                  font_size=11))
        return pop
    
    # Reset previous text fields
    @staticmethod
    def reset_previous():
        sm.screens[0].gmail.text = ''
        sm.screens[0].app_pass.text = ''

    def reset_all(self):
        self.mobile.text = ''
        self.carrier.text = ''
        self.message.text = ''
        self.number.text = '1'

    def reset_message(self):
        self.message.text = ''


class ConfirmScreen(Screen):
    # Declare variables
    gmail = ObjectProperty(None)
    app_pass = ObjectProperty(None)
    message = ObjectProperty(None)
    mobile = ObjectProperty(None)
    carrier = ObjectProperty(None)
    number = ObjectProperty(None)

    # Upon entering this screen, set current diagnostic values
    def on_enter(self, *args):
        g = self.gmail.text = sm.screens[0].gmail.text  # current gmail
        a = self.app_pass.text = sm.screens[0].app_pass.text  # current app_password
        me = self.message.text = sm.screens[1].message.text  # current message
        mo = self.mobile.text = sm.screens[1].mobile.text  # current mobile number
        c = self.carrier.text = sm.screens[1].carrier.text  # current carrier
        n = self.number.text = sm.screens[1].number.text  # current number of messages
        accounts[g]['total'] = int(accounts[g]['total']) + int(n)  # total number of messages sent with account



# Login help
class HelpScreen1(Screen):
    @staticmethod
    def git_link():
        webbrowser.open("https://github.com/Namelocms/Python_SMS#python_sms")

    @staticmethod
    def app_pass_link():
        webbrowser.open("https://support.google.com/accounts/answer/185833?hl=en")


# Send help
class HelpScreen2(Screen):
    @staticmethod
    def git_link():
        webbrowser.open("https://github.com/Namelocms/Python_SMS#python_sms")

    @staticmethod
    def errors_link():
        webbrowser.open("https://www.arclab.com/en/kb/email/"
                        "smtp-response-codes-error-messages.html#:~:"
                        "text=SMTP%20Error%20221&text=Error%20221%20is%20an%20authentication,"
                        "and%20user%2Fpassword%20is%20correct.")

    @staticmethod
    def valid_carriers_pop():
        pop = Popup(title='Valid Carriers',
                    size_hint=(None, None), size=(150, 150),
                    content=Label(text='|  Verizon            \n'
                                       '|  ATT                \n'
                                       '|  TMobile            \n'
                                       '|  Sprint               ',
                                  font_size=15))
        pop.open()

    @staticmethod
    def valid_numbers_pop():
        pop = Popup(title='Valid Numbers',
                    size_hint=(None, None), size=(150, 200),
                    content=Label(text='EX: 1234567890\n\n'
                                       '|  10 Characters\n'
                                       '|  No Spaces\n'
                                       '|  No \'-\'\n'
                                       '|  No Country Code\n'
                                       '|  Yes Area Code',
                                  font_size=15))
        pop.open()


# Confirmed help
class HelpScreen3(Screen):
    @staticmethod
    def git_link():
        webbrowser.open("https://github.com/Namelocms/Python_SMS#python_sms")


# Class name is window name
class SquidSMS(App):
    def build(self):
        self.icon = 'Emphasis.png'
        return sm

    @staticmethod
    def load_json():
        # Open JSON file containing user info
        try:
            file = open('user_data.json')

            # Try to load data from file
            try:
                acc = json.load(file)

            # if there is no data, set accounts to an empty dict
            except json.decoder.JSONDecodeError:
                acc = {}
            file.close()
        # if file non-existent, create it
        except FileNotFoundError:
            file = open('user_data.json', 'w+')
            acc = {}
            file.close()

        return acc

    # load file, setup screen manager
    def on_start(self):
        # Window Configs
        Window.size = (500, 300)
        Window.borderless = 0
        Window.clearcolor = (0.180, 0.180, 0.180, 1.00)

        # Build settings in kivy language
        Builder.load_file(filename='kv_build.kv', encoding='utf8')

        screens = [LoginScreen(name='login'),
                   SendScreen(name='send'),
                   ConfirmScreen(name='confirmed'),
                   HelpScreen1(name='help_login'),
                   HelpScreen2(name='help_send'),
                   HelpScreen3(name='help_confirmed')]

        for screen in screens:
            sm.add_widget(screen)

        sm.current = 'login'

        # Add json data to global accounts dict
        accounts.update(self.load_json())

    # on window close, save accounts to 'user_data.json' file
    def on_stop(self):
        to_json = json.dumps(accounts, indent=4)
        with open('user_data.json', 'w') as outfile:
            outfile.write(to_json)


########################################################################################################################
# Main Loop
########################################################################################################################
if __name__ == "__main__":
    SquidSMS().run()
