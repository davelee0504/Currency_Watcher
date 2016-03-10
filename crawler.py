 #-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from collections import OrderedDict
import sys
import requests
import urllib
import time
from telegram import * # telegram is identical to file name telegram.py
from python_mysql import *

# Currency list from bank of taiwan
crawl_page = "http://rate.bot.com.tw/Pages/Static/UIP003.zh-TW.htm"
output = requests.get(crawl_page)
output = output.text.encode("ISO-8859-1")#weird coding...


soup = BeautifulSoup(output, 'html.parser')
update_time = u"牌價最新掛牌時間\n" + soup.find(style = "width:326px;text-align:left;vertical-align:top;color:#0000FF;font-size:11pt;font-weight:bold;").text.strip()[10:]
#print(update_time)

#現金cash，即期spot，買入buying，賣出selling，遠期forward
currency_dict = OrderedDict()
currencies = soup.find_all("tr", class_ = ["color0", "color1"])
for currency in currencies:
	currency_info = currency.find_all('td')
	currency_name = currency_info[0].text.strip()
	cash_buying_rate = currency_info[2].text.strip()

	if "USD" in currency_name:
		discount_buying_rate = float(cash_buying_rate) - 0.02
	elif "ZAR" in currency_name:
		continue
	elif "VND" in currency_name or "IDR" in currency_name:
		discount_buying_rate = float(cash_buying_rate)
	else:
		discount_buying_rate = float(cash_buying_rate) - (float(cash_buying_rate)*0.001)

	# stored both normal rate and discount rate	
	#currency_dict[currency_name] = str(cash_buying_rate) + '/' + str(discount_buying_rate)

	# stored discount rate only	
	currency_dict[currency_name] = str(discount_buying_rate)

send_msg = update_time + '\n\n'

for currency, rate in currency_dict.iteritems():
	send_msg += (currency + '\t' + rate + "\n")
	
#print send_msg
telegram_client=Telegram()
mysql_client = PythonMysql()
chat_ids = mysql_client.get_subscribe_users()
telegram_client.send_msg(send_msg, chat_ids)




