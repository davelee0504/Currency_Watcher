#-*- coding: utf-8 -*-
import json, requests
from python_mysql import *

config = Config()
token = config.get_telegram_token()
get_updates_url = "https://api.telegram.org/bot%s/getUpdates"%(token)
response = requests.get(get_updates_url)
json_response = json.loads(response.text)

join_string = "/join"
leave_string = "/leave"

isOk = json_response['ok']
result_list = json_response['result']


if(isOk):
	if(len(result_list)):		
		for item in result_list:
			# check if telegram message is text type
			if('text' not in item['message']):
				continue
			text_msg = item['message']['text']
			telegram_user_id = item['message']['from']['id']
			mysql_client = PythonMysql()
			if(text_msg == join_string):
				if(mysql_client.is_user_duplicated(telegram_user_id)):
					print ("user:%s\t text:%s already join the watcher") % (telegram_user_id, text_msg)
				else:
					mysql_client.insert_new_user(telegram_user_id)
					print ("user:%s\t text:%s join the watcher") % (telegram_user_id, text_msg)
			elif(text_msg == leave_string):
				mysql_client.delete_user(telegram_user_id)
				print ("user:%s\t text:%s leave the watcher") % (telegram_user_id, text_msg)

		#print 'result list is empty'

	#print 'I am OK!!'