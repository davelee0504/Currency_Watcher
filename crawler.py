 #-*- coding: utf-8 -*-
import sys
import requests
from collections import OrderedDict
from telegram import * # telegram is identical to file name telegram.py
from python_mysql import *
from bs4 import BeautifulSoup

request = requests.session()
warning_page_source = request.get('https://fctc.bot.com.tw/Purchase/WarningPage#')

soup = BeautifulSoup(warning_page_source.text, 'html.parser')
token =  soup.select('input')[0].get('value')

payload = {
    '__RequestVerificationToken':token
}
currency_page_source = request.post('https://fctc.bot.com.tw/Purchase/SelectCurrencyBank', data = payload)
soup = BeautifulSoup(currency_page_source.text, 'html.parser')

currency_dict = OrderedDict()
update_time=soup.select('h6')[0].text.encode('utf8')
#print update_time

rows = soup.find_all("div", {"class": "m_1"})
for index, tr in enumerate(rows):
        cols=tr.find_all('p')
        currency_name = cols[0].text.replace(u'\xa0','').encode('utf8').strip()
        currency_rate = cols[1].text.encode('utf8').strip()
        #print '%s %s' % (currency_name, currency_rate)
        if currency_name not in currency_dict:
		currency_dict[currency_name] = currency_rate


#print key and value in dictionary
#for key, value in currency_dict.iteritems():
#       print '{0:<15}\t{1: >10}'.format(key, value)

#sys.exit()

send_msg = update_time + '\n\n'
for currency, rate in currency_dict.iteritems():
        send_msg += ('{:<20}'.format(currency) + '\t\t{:>10}'.format(rate) + '\n')
        #print ("%s\t%s")%(key, value)
#print send_msg

telegram_client=Telegram()
mysql_client = PythonMysql()
chat_ids = mysql_client.get_subscribe_users()
telegram_client.send_msg(send_msg, chat_ids)
