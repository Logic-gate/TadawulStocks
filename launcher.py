#!/usr/bin/env python
# -*- coding: utf-8 -*-


# PyStocks v 0.1 - launcher.py
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
import curses
from subprocess import Popen
from sys import exit
import threading
from collections import defaultdict
import ConfigParser
import time
from market.TadawulStocks import *
import re

__author__ = 'Amer Almadani'
__email__ = 'mail@sysbase.org'

class ActionControllerSearch(npyscreen.ActionControllerSimple):
    def create(self):
        npyscreen.setTheme(npyscreen.Themes.TransparentThemeLightText)
        self.add_action('^/.*', self.write2main, True)
    
    def action(self, command, msg):
            current = time.strftime('%c')
            value = [current]
            self.ThreadOpen(command).start()
            value.append(msg)
            self.parent.wMain.values = value

    def write2main(self, command_line, prox, live):
        self.parent.value.set_filter(command_line[1:])
        self.parent.wMain.values = ['Command must start with /']

        emulator = Conf().get('SYS', 'emulator')
        command = Conf().get('SYS', 'command')
        action_geo = Conf().get('ACTION', 'emulator_geo_title')
        main_geo = Conf().get('MAIN', 'emulator_geo_title')
        view_geo = Conf().get('VIEW', 'emulator_geo_title')
        feed_geo = Conf().get('FEED', 'emulator_geo_title')
        if str(command_line) == '/help':
            self.parent.wMain.values = ["refresh: Launch the portfolio refresher(n); n = 10 sec",
                                        "action: Launch the buy and sell window",
                                        "my: Launch your portfolio view",
                                        "stocks: Show all stocks",
                                        "fetch: Fetch prices from Tadawul.com.sa",
                                        "log_sell: Show the sell log",
                                        "log_buy: Show the buy log",]

        elif str(command_line) == '/action':
            self.action('''%s %s %s "python action.py"''' %(emulator, action_geo, command), 'Action has been started. You can buy and sell from it')

        elif str(command_line) == '/refresh':
            self.action('''%s %s %s "python -c 'from refresh import run; run()'"''' %(emulator, main_geo, command), 'Your portfolio is being refreshed every 10 seconds')

        elif str(command_line) == '/my':
            self.action('''%s %s %s "python view.py"''' %(emulator, view_geo, command), 'Your portfolio view has started. Issue fetch command to add new prices')

        elif str(command_line) == '/fetch':
            self.action('''%s %s %s "python feeder.py"''' %(emulator, feed_geo, command), 'Fetching data...')

        elif str(command_line) == '/log_sell':
            log_entry = [line.rstrip('\n') for line in open('log/sell.log')]
            self.parent.wMain.values = log_entry

        elif str(command_line) == '/log_buy':
            log_entry = [line.rstrip('\n') for line in open('log/buy.log')]
            self.parent.wMain.values = log_entry

        elif str(command_line) == '/stock':
            self.parent.wMain.values = GetList('All')

        elif str(command_line) == '/exit':
            exit('Goodbye!')

       
        self.parent.wMain.display()

    
    class ThreadOpen(threading.Thread):


        def __init__(self, cmd):
            threading.Thread.__init__(self)
            self.cmd = cmd

        def run(self):
            Popen(self.cmd, shell=True)


class FmSearchActive(npyscreen.FormMuttActiveTraditional):
    ACTION_CONTROLLER = ActionControllerSearch

class LaunchApp(npyscreen.NPSApp):
    def main(self):
        F = FmSearchActive()
        F.wStatus1.value = "LOG"
        F.wStatus2.value = "COMMAND"
        F.wMain.values = ['Command must start with /','/help for commands']
        F.edit()


if __name__ == "__main__":

    def Conf():
        config = ConfigParser.ConfigParser()
        config.read('conf/info.conf')
        return config

    App = LaunchApp()
    try:
        App.run()
    except KeyboardInterrupt:
        print("Goodbye")

