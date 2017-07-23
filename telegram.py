 #-*- coding: utf-8 -*-

import sys
import requests
import urllib
import time
from config import *

class Telegram:
	config = Config()
	token = config.get_telegram_token()
	method = "sendMessage"

	def send_msg(self, msg, receivers):
		delivery_message = msg		
		for receiver in receivers:
			param_list = {'chat_id' : receiver, 'text' : delivery_message, 'parse_mode': 'Markdown'}
			request_page = "https://api.telegram.org/bot%s/%s?%s"%(self.token, self.method, param_list)
			#print request_page
			time.sleep(1)
			response = requests.get(request_page, param_list)
			print str(receiver) + ' Sent OK.'
			#print response.json()

