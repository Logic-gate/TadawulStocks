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
import re
from bs4 import BeautifulSoup
from market.TadawulStocks import *
import fileinput
import os



__author__ = 'Amer Almadani'
__email__ = 'mail@sysbase.org'

def GetHistoricalData(rangex, rangey, stat, from_year, from_month, from_day, to_year, to_month, to_day):

	'''
	rangex int
	rangey int
	stat FirstTime, Append

	'''
	webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (X11; Linux i686; rv:25.0) Gecko/20100101 Firefox/25.0'
	d = webdriver.PhantomJS('/home/mad-dev/phantomjs-1.9.7-linux-x86_64/bin/phantomjs')
	L = 'http://www.tadawul.com.sa'
	print 'Connecting...'
	d.get(L)
	stock_market_link = d.find_element_by_link_text('سوق الاسهم').click()
	all_stocks_link = d.find_element_by_link_text('جميع الأسهم').click()
	todays_all_stocks_link = d.find_element_by_link_text('جميع الأسهم اليوم').click()
	find_riyadh = d.find_element_by_link_text('الرياض').click()
	stock_prefor = d.find_element_by_link_text('أداء السهم').click()
	find_all = d.find_element_by_class_name('Table3')

	for code in GetCodes('All'):
		for u in range(rangex,rangey):
		    print 'Getting %s | From %s/%s/%s to %s/%s/%s' %(code, from_year, from_month, from_day, to_year, to_month, to_day)
		    yt = d.current_url
		    reg = re.split('(/?symbol=.+)', yt)
		    y = d.get(str(reg[0])+'symbol='+code+'&tabOrder=2&chart_type=chart_oneDay&announcmentNumber=&isAnnual=&isNonAdjusted=0&resultPageOrder='+str(u)+'&totalPagingCount=3120&firstinput='+from_year+'%2F'+from_month+'%2F'+from_day+'&secondinput='+to_year+'%2F'+to_month+'%2F'+to_day)
		    b = d.page_source.encode("utf-8")
		    bs = BeautifulSoup(b)
		    table = bs.find('table', attrs={'class':'Table3'})
		    tbody = table.find('tbody')
		    tr = tbody.find_all('td')
		    listss = []
		    li = []

		    for i in tr:
			    op = listss.extend(i.get_text().split())
		    for ii in listss[14:]:
				li.append(ii)
		    dates = li[0::10]
		    close = li[1::10]
		    openh = li[2::10]
		    high = li[3::10]
		    low = li[4::10]
		    volume = li[7::10]
		    

		    if stat == 'FirstTime':
			    for da, clo, op, hi, lo, vol in zip(dates, close, openh, high, low, volume):
			    	k = {'Date':da, 'Close':clo, 'Open':op, 'High':hi, 'Low':lo, 'Volume':vol}
			    	ribl = open('historical_data/'+code+'.csv', 'a')
			    	ribl.write(k['Date']+','+k['Close']+','+k['Open']+','+k['High']+','+k['Low']+','+k['Volume']+'\n')
			    	ribl.close()

		    elif stat == 'Append':
		    	print 'Appending to', code
		    	for da, clo, op, hi, lo, vol in zip(dates[::-1], close[::-1], openh[::-1], high[::-1], low[::-1], volume[::-1]):
		    		k = {'Date':da, 'Close':clo, 'Open':op, 'High':hi, 'Low':lo, 'Volume':vol}
			        data_write = k['Date']+','+k['Close']+','+k['Open']+','+k['High']+','+k['Low']+','+k['Volume']+'\n'
			        #print data_write
			        origi = open('historical_data/'+code+'.csv')
			        old_data = origi.read()
			        origi.close()
			        origi = open('historical_data/'+code+'.csv', 'w')
			        origi.write(data_write)
			        origi.write(old_data)
			        origi.close()


def FixVolume():
	for code in GetCodes('All'):
		history = open('historical_data/'+code+'.csv', 'r')
		volume_split = re.split('(\d{4}/\d{2}/\d{2},\d{1,}.\d{1,},\d{1,}.\d{1,},\d{1,}.\d{1,},\d{1,}.\d{1,},)', history.read())
		#print volume_split
		history.close()
		correct_volume = []
		orig_withoutV = [x for x in volume_split if x not in volume_split[::2]]
		for i in volume_split[::2]:
		    j = i.replace('\n', '').replace(',','')
		    correct_volume.append(j)
		    
		#print correct_volume
		tre = []
		correct_volume = filter(None, correct_volume) # fastest
		for orig, volume in zip(orig_withoutV, correct_volume):
		    tre.append(orig+volume)
		#print tre
		historyy = open('historical_data/'+code+'.csv', 'w+')
		for ii in tre:
		    #print ii
		    historyy.write(ii+'\n')
		historyy.close()

def DeleteDup():
	for code in GetCodes('All'):
		seen = set()
		for line in fileinput.FileInput('historical_data/'+code+'.csv', inplace=1):
		    if line in seen: continue

		    seen.add(line)
		    print line, 


if __name__ == '__main__':
	GetHistoricalData(1, 2, 'Append', '2014', '11', '1', '2014', '11', '11')
	#print 'Got Data'
	FixVolume()
	#print 'Fixed Volume'
	DeleteDup()
	#print 'Deleted duplicates'