# Author: https://github.com/Namelocms
# Last updated: 01/31/2023
# GitHub Repository: https://github.com/Namelocms/Squid_SMS
# Copyright (c) 2023 Sean Coleman

import smtplib as smt
import datetime as dt
from colorama import Fore, Style

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
				print(Fore.GREEN + 'Login Successful' + Style.RESET_ALL)
				return server

			else:
				raise smt.SMTPAuthenticationError

		except smt.SMTPAuthenticationError:
			print(Fore.RED + Style.BRIGHT)
			print('===============================================================================================')
			print('SMS SEND FAILED:\nError: SMTPAuthenticationError: Email/Password Incorrect\n'
				  'Email:\n  {}\n'
				  'Date:\n  {}'.format(self.AUTH_EMAIL, dt.datetime.now()))
			print('===============================================================================================')

			# self.server.quit()  # end server connection
			print(Fore.RED + Style.BRIGHT + 'SMTP Server Connection Ended!')
			print(Style.RESET_ALL)

			return server.quit()  # end server connection

	def send(self, phone_number, carrier, message):
		# server is returned as type tuple() on disconnect, so if not disconnected, continue
		if type(server) is not tuple:	
			try:
				if not self.check_phone_number(phone_number) or not self.check_carrier(carrier):
					raise ValueError
				else:
					# convert phone_number and carrier into usable string
					recipient = "{} {}".format(phone_number, self.CARRIERS[carrier])
					
					try:
						# Send text message through SMS gateway of destination number
						server.sendmail(auth[0], recipient, message)
						print(Fore.GREEN + 'Send Successful' + Style.RESET_ALL)
						return True

					except (smt.SMTPAuthenticationError, AttributeError):
						print(Fore.RED + Style.BRIGHT)
						print('===============================================================================================')
						print('SMS SEND FAILED:\nError: Email/Password Incorrect\n'
							  'Email:\n  {}\n'
							  'Password:\n  {}\n'
							  'Recipient:\n  {}::{}\n'
							  'Message:\n  {}\n'
							  'Date:\n  {}'.format(self.AUTH_EMAIL, self.AUTH_PASS, phone_number, carrier, message, dt.datetime.now()))
						print('===============================================================================================')
						print(Style.RESET_ALL)
						
						# In case connection is ended already
						try:
							self.disconnect(server)
						except AttributeError:
							pass
						return False

			except ValueError:
				print(Fore.RED + 'Invalid Recipient/Carrier Information')
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
		print(Fore.RED + Style.BRIGHT + 'SMTP Server Connection Ended!')
		print(Style.RESET_ALL)

	# Ensure provided number formatting is correct,
	# wont check if number is real or not
	@staticmethod
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
	def check_carrier(self, carrier):
		if carrier in self.CARRIERS:
			print(Fore.GREEN + carrier + ' is valid' + Style.RESET_ALL)
			return True
		print(Fore.RED + carrier + ' is invalid' + Style.RESET_ALL)
		return False
