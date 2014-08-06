#!/usr/bin/env python
# -*- coding: utf-8 -*-


# PyStocks v 0.1 - refresh.py
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

from decimal import *
from prettytable import PrettyTable
import ConfigParser
import sys
import sched, time


__author__ = 'Amer Almadani'
__email__ = 'mail@sysbase.org'


timer = sched.scheduler(time.time, time.sleep)

def MyStock():
    my_stocks = GetConfig('code')[0]
    stock_code = GetConfig('code')[1]
    stock_prices = []
    for i in my_stocks:
        if Config('Get').has_option(i, 'last_price') == True:
            stock_prices = GetConfig('last_price')[1]
            if '0.00' in stock_prices:
                sys.exit('Try Updating The Price List')
            
        else:
            print 'Error'
    buying_price = GetConfig('last_buying_price')[1]
    my_shares = GetConfig('shares')[1]
    last_purchase_date = GetConfig('last_purchase_date')[1]
    getcontext().prec = 3
    tot = PrettyTable(["Portfolio Worth"])
    tot.padding_width = 14
    total_worth = sum([float(price)*int(shares) for price,shares in zip(stock_prices, my_shares)])
    tot.add_row([str(total_worth) + " SAR"])
    #print tot
    #print '\n'
    t = PrettyTable(["Code", "Name", "Price", "Shares", "Total", "% of Net Worth", "Buying Price", "% of Profit", "Last Purchase Date"])
    t.float_format = "4.2"
    t.padding_width = 1
    for code, name, price, shares, buy_price, purch in zip(stock_code, my_stocks, stock_prices, my_shares, buying_price, last_purchase_date):
        total = float(price) * int(shares)
        perce = float(total) / int(total_worth) * 100
        profit = (Decimal(price) - Decimal(buy_price)) / Decimal(buy_price) * 100
        t.add_row([code, name, str(price) + ' SAR', shares, str(total) + " SAR", perce, str(buy_price) + " SAR", profit, purch])
    print 'Refreshing Portfolio...'
    return tot, t


def Config(option):
    config = ConfigParser.ConfigParser()
    if option == 'Set':
        configFile = open('conf/stocks.conf', 'a')
        return configFile, config
    elif option == 'Get':
        config.read('conf/stocks.conf')
        return config

def GetConfig(option):
    stock_info = []
    config = Config('Get')
    section = config.sections()
    for i in section:
        stock_info.append(config.get(i, option))
        pass
    return section, stock_info 
        #for ii in config.options(i):
            #print ii
            #stock_info = config.get(i, ii) 
        #return section, stock_info

def SetConfig(stock_name, code, shares, last_buying_price, last_purchase_date, last_price):
    config = Config('Set')[1]
    configFile = Config('Set')[0]
    config.add_section(stock_name)
    config.set(stock_name,'code', code)
    config.set(stock_name,'last_price', last_price)
    config.set(stock_name,'shares', shares)
    config.set(stock_name,'last_buying_price', last_buying_price)
    config.set(stock_name,'last_purchase_date', last_purchase_date)
    config.write(configFile)

def SetLast(param, value, stock_name):
    config = ConfigParser.RawConfigParser()
    config.read('conf/stocks.conf')
    if param == 'Price':
        config.set(stock_name, 'last_price', value)
    elif param == 'Shares':
        config.set(stock_name, 'shares', value)
    elif param == 'Last_Buying_Price':
        config.set(stock_name, 'last_buying_price', value)
    elif param == 'Last_Purchase_Date':
        config.set(stock_name, 'last_purchase_date', value)

    with open('conf/stocks.conf', 'w') as configfile:
        config.write(configfile)


def Write_(data):
    path = 'log/MyStock.li'
    x = open(path, 'w+')
    x.write(data)
    x.close()
    print 'MyStock.li Saved %s\n' %time.time()


def repeat(fun): 
    my_stock = MyStock()
    Write_(str(my_stock[0])+'\n'+str(my_stock[1]))
    fun.enter(10, 1, repeat, (fun,))


def run():
    timer.enter(10, 1, repeat, (timer,))
    timer.run()
 