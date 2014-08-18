#!/usr/bin/env python
# -*- coding: utf-8 -*-


# TadawulStocks v 0.1 - feeder.py
# Copyright (C) <2014>  mad_dev(A'mmer Almadani)
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL A'MMER ALMADANI BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Report any issues with this script to <mad_dev@linuxmail.org>


from selenium import webdriver
import time
from market.TadawulStocks import *
import ConfigParser
from refresh import Config, GetConfig, SetLast


__author__ = 'Amer Almadani'
__email__ = 'mail@sysbase.org'


def Conf():
        config = ConfigParser.ConfigParser()
        config.read('conf/info.conf')
        return config

def Search(Tadawul_code, sector):
	'''
	Search(list(Tadawul_code), str(sector)) -> number

	number: as per the return from find_all in Feeder(list(stock))
	'''
	code_lists = []
	name_lists = []
	for i in Tadawul_code:
		data = GetData(i, TadawulStocks(sector))
		name = data[0]
		number = data[1]
		code = data[2]
		last_price = int(number)
		#print name
		code_lists.append(last_price)
		name_lists.append(name)
	#print code_lists
	return name_lists, code_lists

def Feeder(stock):
	'''
	Feeder(list(stock)) -> last price and volume

	stock: list if stock codes
	'''
	print 'Starting Systems'
	phantomJS = Conf().get('SYS', 'phantomJS')
	webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (X11; Linux i686; rv:25.0) Gecko/20100101 Firefox/25.0'
	d = webdriver.PhantomJS(phantomJS)


	#print 'Obtained phantomJS'
	L = 'http://www.tadawul.com.sa'
	print 'Connecting...'
	time.sleep(5)
	d.get(L)
	stock_market_link = d.find_element_by_link_text('سوق الاسهم').click()
	
	all_stocks_link = d.find_element_by_link_text('جميع الأسهم').click()
	time.sleep(0.5)
	todays_all_stocks_link = d.find_element_by_link_text('جميع الأسهم اليوم').click()
	time.sleep(0.5)
	find_all = d.find_elements_by_class_name('calibri-12')
	#print find_all
	time.sleep(0.5)
	print 'Fetching...'
	configGet = Config('Get')
	#print stock
	for ii, i in zip(configGet.sections(), stock):
		#print ii, i
		if configGet.has_section(ii) == True:
				last_price = find_all[int(i)].text
				last_vol =  find_all[int(i)+1].text
				SetLast('Price', last_price, ii)
	d.close()
	#return find_all

def GetInfo(Tadawul_code, sector):
	feed = Feeder()
	last_price = feed[int(Search(Tadawul_code, sector))].text
	last_vol =  feed[int(Search(Tadawul_code, sector))+1].text
	#print last_price
	#print last_vol


def SetLastData(stock_name, last_price):
	config = Config('Set')[1]
	configFile = Config('Set')[0]
	config.set(stock_name,'last_price', last_price)
	#config.set(stock_name,'last_volume', last_volume)
	config.write(configFile)

	
if __name__ == '__main__':
	list_of = GetConfig('code')[1]
	Feeder(Search(list_of, 'All')[1])


