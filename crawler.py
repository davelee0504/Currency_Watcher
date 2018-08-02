#coding=utf-8
import sys
import requests
from collections import OrderedDict
from telegram import * # telegram is identical to file name telegram.py
from python_mysql import *
from bs4 import BeautifulSoup


class Crawler(object):
    updated_time = ''
    buy_price_dict = OrderedDict()
    sell_price_dict = OrderedDict()
    currency_name_dict = {}
    '''bank perspective'''
    def crawl_buy_price(self):
        buy_price_source = requests.get('http://rate.bot.com.tw/xrt?Lang=zh-TW')
        source_soup = BeautifulSoup(buy_price_source.text, 'html.parser')

        
        rows = source_soup.select('tr')
        for index, tr in enumerate(rows):
                currency_name = tr.find_all('div', {"style": "text-indent:30px;"})
                currency_rate = tr.find_all('td', {"data-table": "本行即期買入"})
               
                if currency_name and currency_rate:
                    currency_name = currency_name[0].text.strip()
                    currency_rate = currency_rate[0].text.strip()
                    

                    if currency_name not in self.buy_price_dict:
                        # get currency names
                        eng_currency_name = currency_name[-4:].replace('(','').replace(')', '')
                        chi_currency_name = currency_name[:-5]
                        self.currency_name_dict[eng_currency_name] = chi_currency_name
                        self.buy_price_dict[eng_currency_name] = currency_rate
                        

    def crawl_sell_price(self):
        request = requests.session()
        warning_page_source = request.post('https://fctc.bot.com.tw/Purchase/WarningPage#')
        
        soup = BeautifulSoup(warning_page_source.text, 'html.parser')
        token =  soup.select('input')[0].get('value')
        
        payload = {
            '__RequestVerificationToken':token
        }
        currency_page_source = request.post('https://fctc.bot.com.tw/Purchase/SelectCurrencyBank', data = payload)
        soup = BeautifulSoup(currency_page_source.text, 'html.parser')

        self.updated_time=soup.select('h6')[0].text

        rows = soup.find_all("div", {"class": "m_1"})
        for index, tr in enumerate(rows):
                cols=tr.find_all('p')
                currency_name = cols[0].text.replace(u'\xa0','').strip()
                currency_rate = cols[1].text.strip()
                if len(currency_rate) > 7:
                    currency_rate = currency_rate[:6]
                
                if currency_name not in self.sell_price_dict:
                    self.sell_price_dict[currency_name[-3:]] = currency_rate
                   
    def send_rates(self):
        send_msg = c.updated_time.encode('utf-8') + '\n\nSpot Rate Buy/Cash Rate Sell\n\n'
        for currency, rate in c.buy_price_dict.iteritems():
            # buy_price_dict has full list of currency, so no need to check
            if not c.sell_price_dict.has_key(currency):
                c.sell_price_dict[currency] = '-'    
            formatted_name = '*{0}({1})*'.format((c.currency_name_dict[currency]).encode('utf-8'), currency)
            send_msg += '{0:25}{1:>6} / {2:>6}\n'.format(formatted_name, c.buy_price_dict[currency], c.sell_price_dict[currency]) 
           
        telegram_client=Telegram()
        mysql_client = PythonMysql()
        chat_ids = mysql_client.get_subscribe_users()
        telegram_client.send_msg(send_msg, chat_ids)

c = Crawler()
c.crawl_buy_price()
c.crawl_sell_price()
c.send_rates()
