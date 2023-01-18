# Author: https://github.com/Namelocms
# Last updated: 01/18/2023
# GitHub Repository: https://github.com/Namelocms/Python_SMS

import smtplib as smt
import datetime as dt
from colorama import Fore, Style

########################################################################################################################
#                                                 CONSTANTS
########################################################################################################################
# Cellular Service Providers
CARRIERS = {
	'att':      '@mms.att.net',
	'Att':		  '@mms.att.net',
	'ATT':		  '@mms.att.net',

	'tmobile':  '@tmomail.net',
	'Tmobile':	'@tmomail.net',
	'TMobile':	'@tmomail.net',
	'TMOBILE':	'@tmomail.net',

	'verizon':  '@vtext.com',
	'Verizon':  '@vtext.com',
	'VERIZON':  '@vtext.com',

	'sprint':   '@page.nextel.com',
	'Sprint':   '@page.nextel.com',
	'SPRINT':   '@page.nextel.com'
}

# Email to use in sending the SMS
AUTH_EMAIL = 'YourEmailHere@gmial.com'

# App Password (not email password) for 'AUTH_EMAIL'
AUTH_PASS = 'AppPasswordHere'
########################################################################################################################


def send(phone_number, carrier, message):
	try:
		if not check_phone_number(phone_number) or not check_carrier(carrier):
			raise ValueError
		else:
			# convert phone_number and carrier into usable string
			recipient = "{} {}".format(phone_number, CARRIERS[carrier])

			# Email + Password used to send message
			auth = (AUTH_EMAIL, AUTH_PASS)

			try:
				# Establish a secure session with gmail's outgoing SMTP server using your gmail account
				server = smt.SMTP("smtp.gmail.com", 587)
				server.starttls()
				if server.login(auth[0], auth[1]):
					print(Fore.GREEN + 'Login Successful' + Style.RESET_ALL)
				else:
					raise smt.SMTPAuthenticationError

				# Send text message through SMS gateway of destination number
				server.sendmail(auth[0], recipient, message)
				print(Fore.GREEN + 'Send Successful' + Style.RESET_ALL)

			except smt.SMTPAuthenticationError:
				print(Fore.RED + Style.BRIGHT)
				print('===============================================================================================')
				print('SMS SEND FAILED:\nError: SMTPAuthenticationError: Email/Password Incorrect\n'
					  'Email:\n  {}\n'
					  'Recipient:\n  {}::{}\n'
					  'Message:\n  {}\n'
					  'Date:\n  {}'.format(AUTH_EMAIL, phone_number, carrier, message, dt.datetime.now()))
				print('===============================================================================================')
				print(Style.RESET_ALL)
				return False

	except ValueError:
		print(Fore.RED + 'Invalid Recipient/Carrier Information')
		return False

	return True


# Ensure provided number formatting is correct,
# wont check if number is real or not
def check_phone_number(phone_number):
	if len(phone_number) == 10:
		try:
			int(phone_number)	# is number?
			print(Fore.GREEN + phone_number + ' is valid' + Style.RESET_ALL)
			return True
		except ValueError:
			print(Fore.RED + phone_number + ' is invalid' + Style.RESET_ALL)
			return False
	else:
		print(Fore.RED + phone_number + ' is invalid' + Style.RESET_ALL)
		return False


# Check carrier is valid
def check_carrier(carrier):
	for c in CARRIERS:
		if c == carrier:
			print(Fore.GREEN + carrier + ' is valid' + Style.RESET_ALL)
			return True
	print(Fore.RED + carrier + ' is invalid' + Style.RESET_ALL)
	return False
