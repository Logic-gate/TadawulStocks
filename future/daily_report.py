html = urllib2.urlopen('http://www.tadawul.com.sa/Resources/Reports/DetailedDaily_en.html').read()
bs = BeautifulSoup(html)
table = bs.find('table', {'class':'Table2'})
#print table
tbody = table.find('tbody')
tr = tbody.find_all('tr')
listss = []
li = []
for i in tr:
    data = i.get_text().replace(',', '').split()
    op = listss.extend(data)
#print listss    
openh = listss[1]
high = listss[3]
low = listss[5]
close = listss[7]
change = listss[9]
change_perc = listss[12]
companies_traded = listss[15]
trades = listss[18]
volume = listss[20]
value = listss[22]

#for o, h, l, c, ch, chp, ct, t, v, val in zip(openh, high, low, close, change, change_perc, companies_traded, trades, volume, value):
dic = {'Open':openh, 'High':high, 
        'Low':low,'Close': close, 
        'Change':change, 'Change%': change_perc,
         'Companies_Traded': companies_traded, 
        'Trades': trades, 'Volume': volume, 'Value': value}
    
print dic['Open']
print dic

#tr = tbody.find('tr', {'class':'table_noback'})
#tr