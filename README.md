TadawulStocks
======
 
A minimalistic Python based portfolio manager.

This version only supports the saudi stock exchange (Tadawul)
***

Intsallation 
---  

**Python** 

```
pip install -r requirements.txt
```
*cat requirements.txt*
```
argparse==1.2.1
configparser==3.3.0r2
npyscreen==4.3.5
prettytable==0.7.2
selenium==2.42.1
wsgiref==0.1.2
```
---

PyStocks relies on phantomJS for retrieving Tadawul's market data.  
Go to http://phantomjs.org/download.html and download your box's version.  


**info.conf**  
Navigate to ***conf/info.conf*** and fill in the ***phantomJS*** option with the path to your phantomJS executable.  
```
[SYS]
emulator=xterm
command=-e
phantomJS=/path/to/phantomjs-x.x.x-linux-xxx-xx/bin/phantomjs

```

***

How TO
---
Assuming you installed all the prerequisites, open a terminal in the **PyStocks** directory and type:
```
python launcher.py
```
You will be presented with a *mutt* like window. The top section is the **log** view, the bottom, the **command** view. Type
```
/help

```
The **log** view should return all available commands
```
refresh: Launch the portfolio refresher(n); n = 10 sec
action: Launch the buy and sell window
my: Launch your portfolio view
stock: Show all stocks
fetch: Fetch prices from Tadawul.com.sa
log_sell: Show the sell log
log_buy: Show the buy log
```

Note: You must use a slash before issuing the command
```
/
```
Issue the action command
```
/action
```
A new terminal should popup with with two options
```
Option      (X)Buy
            ( )Sell
```
Go through the process and buy your stocks.

If you wish to search for stocks.
In the **command** view(the one you launched the **/action** command with) type
```
/stock
```
A list of all Tadawul stocks will render in the **log** view. Press **lower_case(L)** l. A contained popup will appear for you to search with. Type the name of the stock you wish to find; only upper case search is allowed.

Issue the refresh command
```
/refresh
```
Note: **refresh** must be issued before **my**

Issue the portfolio view command
```
/my
```
You will notice that the price is set 1 SAR; all new stocks will have a price of 1 SAR to them. You will need to issue the fetch command in order to get the latest price from tadawul.com.sa
```
/fetch
```
Note: On average it will take 2 minutes to fetch the data. The delay is from Tadawul and my method of retrieving data.

All of your activities can be viewed by issuing the log commands
```
/log_buy
```
&
```
/log_sell
```

***
Detailed Architecture 
---

**Tree View**
```
PyStocks
|
├── conf
│   ├── info.conf
│   └── stocks.conf
├── future
│   └── chart.py
├── log
│   ├── buy.log
│   ├── MyStock.li
│   └── sell.log
├── market
│   ├── __init__.py
│   └── TadawulStocks.py
├── rss
│   ├── feeds.db
│   └── rss.py
├── action.py
├── feeder.py
├── launcher.py
├── LICENSE
├── README.md
├── refresh.py
├── requirements.txt
└── view.py

```
***
###**conf**

As the name suggests, *conf* contains the config files:  

1. info.conf
2. stocks.conf

**info.conf** contains basic operation options.

```
# Adjust the values as you see fit.

[SYS]
emulator=xterm
command=-e
phantomJS=

[ACTION]
emulator_geo_title =-T "Buy'nSell" -geometry 100x50+0+100 -bg grey24

[MAIN]
emulator_geo_title =-T "Portfolio Refresher" -geometry 30x24-0+50 -bg grey24

[VIEW]
emulator_geo_title=-T "My Stocks" -geometry 150x40+750+100 -bg grey24

[FEED]
emulator_geo_title=-T "Feeder" -geometry 30x24-0-50

```
The ***emulator*** option under the **SYS** section should be filled with the desired terminal emulator of your choosing. The ***command*** option is the parameter by which the emulator launches programs with in a new window. ***xterm*** is the default emulator.  

As stated in the aforementioned installation section of this document, the ***phantomJS*** option should be filled with the path to your phantomJS binary file. You can find it under the ***phantomjs-x.x.x-linux-xxx-xx/bin/*** directories.  

The **ACTION, MAIN, VIEW,** and **FEED** sections contain the emulator's title and geometry settings. These are relative to the emulator in use; if you changed the emulator to *terminator* for example, you will need to adjust the values of the ***emulator_geo_title*** option as well. You can also change the foreground and background colours to your liking; please refer to your emulator's documentation for more information on customizing it. The latter and former sections(except ***phantomJS***) are required by **launcher.py**.
***
The **stocks.conf** contains information retaining your stocks. It should not be edited manually, **action.py** and **feed.py** will take care of everything.  

Example of **stocks.conf**
```
[Jarir]
code = 4190
last_price = 200
shares = 100
last_buying_price = 198
last_purchase_date = 2014-07-01
```
Sections are named after the stock. The **code** option refers to Tadawul's code system of arranging stocks. **last_price** is the last the price retrieved from tadawul.com.sa. The rest of the options are self-explanatory.
***
###log

The **log** directory contains the log files:

1. MyStock.li
2. buy.log
2. sell.log

**MyStock.li** is a file that is written to by **refresh.py** in order for **view.py** to render it in a continuous viewable form.

**buy.log** and **sell.log** register your activity accordingly.
***
###market
The **market** directory was created to house multiple stock markets; the idea was to create a packaged directory that could be imported.
```
from market.USAStocks import *
from market.UKStocks import *
#and so on
```
Currently, the only market available is the Saudi Stock Exchange (Tadawul). The former market is defined in **TadawulStocks.py**. For future markets, I will refrain from using the method used to retrieve market data from Tadawul. Seeing as how they lack an API, I was forced to use **phantomJS** as the mean for achieving my goal. You can find further information by viewing the source code.
***
###action.py
**action.py** takes care of buying and selling stocks. For buying stocks, it has two options:

1. By Code
2. Choose from list

Saves all data to **stocks.conf**

***

###feeder.py
**feeder.py** will retrieve your stock's last price from tadawul.com.sa.  

Saves the ***last_price*** to **stocks.conf**  

It could be improved. +[TODO]


***
###launcher.py
All scripts are launched through it.

The commands are as follows:
```
refresh: Launch the portfolio refresher(n); n = 10 sec
action: Launch the buy and sell window
my: Launch your portfolio view
stock: Show all stocks
fetch: Fetch prices from Tadawul.com.sa
log_sell: Show the sell log
log_buy: Show the buy log
```

All commands must start with a slash
```
/
```

When the **Log** view is focused, you can search its contents by pressing on **lower_case(L)**

***
###refresh.py & view.py
**refresh.py** takes care of creating the tables by which **view.py** relies on to represent. The default refresh period is 10 seconds.

Just to clarify, **refresh.py** writes the rendered table(stocks) to **MyStock.li** every 10 seconds. **view.py** reads **MyStock.li** every 10 seconds. Future versions will see the end of **refresh.py**

***
###future & rss directories
Meant for future improvements to **PyStocks**
