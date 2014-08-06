#!/usr/bin/env python
# -*- coding: utf-8 -*-


# PyStocks v 0.1 - action.py
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
from __future__ import absolute_import
import npyscreen
from market.TadawulStocks import *
from refresh import SetConfig, GetConfig, SetLast, Config
import re

__author__ = 'Amer Almadani'
__email__ = 'mail@sysbase.org'

class TestApp(npyscreen.NPSAppManaged):
    def main(self):
        npyscreen.setTheme(npyscreen.Themes.TransparentThemeLightText)
        buy_sell  = npyscreen.Form(name = "Buy & Sell Stocks",)
        pick  = buy_sell.add(npyscreen.TitleFixedText, name = "Please choose an option",)
        option= buy_sell.add(npyscreen.TitleSelectOne, max_height =-2, value = [1,], name="Option",
                values = ["Buy","Sell"], scroll_exit=True)
        
        buy_sell.edit()
        if str(option.get_selected_objects()) == "['Buy']":
            self.buy()
        elif str(option.get_selected_objects()) == "['Sell']":
            self.sell()

    def buy(self):
        stocks = GetList('All')
        my_stocks = GetConfig('code')[0]
        my_shares = GetConfig('shares')[1]
        config = Config('Get')
        buy_log = open('log/buy.log', 'a')


        code_list  = npyscreen.Form(name = "Buy Code Or List",)

        pick  = code_list.add(npyscreen.TitleFixedText, name = "Please choose an option",)
        option = code_list.add(npyscreen.TitleSelectOne, max_height =-2, value = [1,], name="Option",
                values = ["Tadawul Code","Choose From List"], scroll_exit=True)
        code_list.edit()

        if str(option.get_selected_objects()) == "['Choose From List']":

            list_  = npyscreen.Form(name = "Buy - List",)
            stock = list_.add(npyscreen.TitleSelectOne, max_height=30, value = [1,], name="Stocks", values = stocks, scroll_exit=True)
            shares = list_.add(npyscreen.TitleText, name = "Shares:",)
            price = list_.add(npyscreen.TitleText, name = "Price:",)
            date = list_.add(npyscreen.TitleDateCombo, name = "Date:")

            list_.edit()

            code = str(stock.get_selected_objects())
            code_re = re.findall('[0-9]{1,}', code)[0]

            if re.findall('[\w]{1,}', code)[0] in config.sections():
                section = re.findall('[\w]{1,}', code)[0]
                aval = Config('Get').get(section, 'shares')
                current_shares = int(aval) + int(shares.value)

                SetLast('Shares', current_shares, section)
                SetLast('Last_Buying_Price', price.value, section)
                SetLast('Last_Purchase_Date', date.value, section)

            else:    
                SetConfig(stock_name=GetData(code=code_re, sector=TadawulStocks('All'))[0],
                          code=code_re,
                          shares=shares.value,
                          last_buying_price=price.value,
                          last_purchase_date=date.value,
                          last_price=1)

            stock_code = code_re

            
        elif str(option.get_selected_objects()) == "['Tadawul Code']":

            code = npyscreen.Form(name = "Buy - List",)
            stock = code.add(npyscreen.TitleText, name = "Code:",)
            shares = code.add(npyscreen.TitleText, name = "Shares:",)
            price = code.add(npyscreen.TitleText, name = "Price:",)
            date = code.add(npyscreen.TitleDateCombo, name = "Date:",)

            code.edit()

            if re.findall('[\w]{1,}', GetData(code=stock.value, sector=TadawulStocks('All'))[0])[0] in config.sections():
                section = re.findall('[\w]{1,}', GetData(code=stock.value, sector=TadawulStocks('All'))[0])[0]
                aval = Config('Get').get(section, 'shares')
                current_shares = int(aval) + int(shares.value)

                SetLast('Shares', current_shares, section)
                SetLast('Last_Buying_Price', price.value, section)
                SetLast('Last_Purchase_Date', date.value, section)
            else:
            
                SetConfig(stock_name=GetData(code=stock.value, sector=TadawulStocks('All'))[0],
                          code=stock.value,
                          shares=shares.value,
                          last_buying_price=price.value,
                          last_purchase_date=date.value,
                          last_price=1)

            stock_code = stock.value

        total = float(shares.value) * float(price.value)
        string = "%s - You Bought %s shares of %s for %s SAR per share. %s SAR in total." %(date.value, shares.value, GetData(code=stock_code, sector=TadawulStocks('All'))[0], price.value, str(total))
        buy_log.write(string+'\n')
        buy_log.close()

    def sell(self):
        my_stocks = GetConfig('code')[0]
        my_shares = GetConfig('shares')[1]
        sell_log = open('log/sell.log', 'a')
      #  stock_shares = []
     #   for stocks, share in zip(my_stocks, my_shares):
    #        stock_shares.append(stocks + ' - Shares = ' +share)

        sell  = npyscreen.Form(name = "Sell",)
        pick  = sell.add(npyscreen.TitleFixedText, name = "Select a stock to sell",)
        option = sell.add(npyscreen.TitleSelectOne, max_height =5, value = [1,], name="My Stocks",
                values = my_stocks, scroll_exit=True)
        

        shares = sell.add(npyscreen.TitleText, name = "Shares:", rely=9)
        price = sell.add(npyscreen.TitleText, name = "Price:",)
        date = sell.add(npyscreen.TitleDateCombo, name = "Date:",)
        sell.edit()
        
        selected_stock = str(option.get_selected_objects())
        
        stock = re.findall('[\w]{1,}', selected_stock)
        for i in stock:
            try:
                aval = Config('Get').get(i, 'shares')
                current_shares = int(aval) - int(shares.value)
                
            except:
                current_shares = int(aval) - int(0)
                #self.Notify('No value was set')

        SetLast('Shares', current_shares, i)
        total = float(shares.value) * float(price.value)
        string = '%s - You Sold %s shares of %s for %s SAR. You made %s SAR' %(date.value, shares.value, i, price.value, total)
        sell_log.write(string+'\n')
        sell_log.close()

    def Notify(self, msg):
        npyscreen.notify_confirm(msg, title='Error')



if __name__ == "__main__":
    #npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
    App = TestApp()
    while 1:
        try:
            App.run()
        except KeyboardInterrupt:
            break
            print("Goodbye")