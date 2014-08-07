#!/usr/bin/env python
# -*- coding: utf-8 -*-


# TadawulStocks v 0.1 - view.py
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
import npyscreen
from datetime import datetime
from refresh import GetConfig, run
import sys

__author__ = 'Amer Almadani'
__email__ = 'mail@sysbase.org'

list_of = GetConfig('code')[1]

def read_():

    data = open('log/MyStock.li', 'r')
    ret = data.read()
    data.close()
    return ret
class StockForm(npyscreen.FormBaseNew):
    def while_waiting(self):
        self.read_stocks.value = read_()
        self.display()
        

    def create(self):
        npyscreen.setTheme(npyscreen.Themes.TransparentThemeLightText)
        npyscreen.notify_confirm('Your portfolio will be refreshed every 10 seconds')
        self.read_stocks = self.add(npyscreen.MultiLineEdit, value=read_(), editable=True)

    def cleanExit(self):

        self.read_stocks.value = sys.exit()
        

class StockApp(npyscreen.NPSAppManaged):

    keypress_timeout_default = 10

    def onStart(self):
        
        self.addForm("MAIN", StockForm, name="My Stocks ")        





if __name__ == '__main__':
    app = StockApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print("Goodbye")
    
