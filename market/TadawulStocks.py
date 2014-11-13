#!/usr/bin/env python
# -*- coding: utf-8 -*-


# TadawulStocks v 0.1 - TadawulStocks.py
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
from collections import defaultdict

__author__ = 'Amer Almadani'
__email__ = 'mail@sysbase.org'

#TRADEUNION SF
def TadawulStocks(sector):
	'''
	stocks(str(sector)) -> sector list

	Sector:
		All 		All Sectors -- use this instead of specific sectors
		Banks 		Banks & Financial Services
		Petro 		Petrochemical Industries
		Cement 		Cement
		Retail 		Retail
		Energy 		Energy & Utilities
		Agri_Food 	Agriculture & Food Industries
		Tele		Telecommunication & Information Technology
		Insurance	Insurance
		Invest 		Multi-Investment 
		Indust      Industrial Investment
		Build		Building & Construction
		Estate		Real Estate Development
		Transport	Transport
		Media		Media and Publishing
		Hotel		Hotel & Tourism 

		For more on Sectors: tadawul.com.sa

		If no sector is declared, assume All

	List Format(Company Acronym:List Number:Comapny Code):
		
		Company Acronym:  Not be confused with SHORT NAME
			Example:
			    COMPANY NAME -> Al-Jouf Agriculture Development Co.
			    SHORT NAME -> ALJOUF
			    ACRONYM -> JADCO 

		List Number: As per the return from find_all in feeder.py.
		             find_all[List Number].text will return the contents of what is inside class_name(html) calibri-12.
		             Tadawul.com.sa uses the same class_name for the name, price, and volume.

		             Issues with using the class_name(html) method: 
		             If Tadwul.com.sa were to add a new stock, I'll need to construct a new list.

		Company Code: Tadawul calls it SYMBOL. 
		              Please check tadawul.com.sa for more info.			

	'''
	banks = ['SaudiInvestment:93:1030',
	 		 'SaudiHollandi:107:1040',
	 		 'SABB:135:1060',
	 		 'ARNB:149:1080',
	 		 'ALINMA:205:1150',
	 		 'RJHI:177:1120',
	 		 'ALBI:191:1140',
	 		 'BJAZ:79:1020',
	 		 'BSFR:121:1050',
	 		 'SAMBA:163:1090',
	 		 'RIBL:65:1010',
	 		 'ALAHLI:219:1180']

	petro = ['Advanced:389:2330', 
					 'ALCO:305:2170',
					 'CHEMANOL:235:2001',
					 'NAMA:319:2210',
					 'NIC:291:2060',
					 'Petrochem:249:2002',
					 'PETRORABIGH:417:2380',
					 'SPC:347:2260',
					 'SAFCO:277:2020',
					 'SABIC:263:2010',
					 'SIIG:333:2250',
					 'SIPCHEM:375:2310',
					 'KAYAN:403:2350',
					 'YANSAB:361:2290']

	cement = ['JoufCement:615:3091',
			  'ARCCO:503:3010',
			  'CityCement:461:3003',
			  'EACCO:587:3080',
			  'HCC:433:3001',
			  'NajranCement:447:3002',
			  'NorthenCement:475:3004',
			  'SACCO:531:3030',
			  'SOCCO:559:3050',
			  'TACCO:601:3090',
			  'QACCO:545:3040',
			  'UACC:489:3005',
			  'YACCO:517:3020',
			  'YNCCO:573:3060']

	retail = ['AOTHAIMMARKET:631:4001',
			  'AlHammadi:715:4007',
			  'ALDREED:785:4200',
			  'ALKHALEEJTRNG:813:4290',
			  'DallahHealth:673:4004',
			  'ALHOKAIR:799:4240',
			  'AHFCO:757:4180',
			  'Jarir:771:4190',
			  'Mouwasat:645:4002',
			  'THIMAR:743:4160',
			  'Care:687:4005',
			  'SASCO:729:4050',
			  'FarmSuperstore:701:4006',
			  'Extra:659:4003']

	energy = ['NGIC:829:2080',
			  'SECO:843:5110']

	agri_food = ['JADCO:985:6020',
				 'ALMARAI:901:2280',
				 'ANAAMHOLDING:915:4061',
				 'SHARQIYADEVCO:1027:6060',
				 'BISACO:1055:6080',
				 'HB:929:6001',
				 'HerfyFoods:943:6002',
				 'GIZACO:1069:6090',
				 'NADEC:971:6010',
				 'QAACO:985:6020',
				 'Catering:957:6004',
				 'SFICO:1013:6050',
				 'SADAFCO:887:2270',
				 'SAVOLA:859:2050',
				 'TAACO:999:6040',
				 'FPCO:873:2100']

	tele = ['ATHEEBTELECOM:1127:7040',
			'EEC:1099:7020',
			'ZAINKSA:1113:7030',
			'Almutakamela:1141:7050',
			'STC:1085:7010']

	insurance = ['ACE:1507:8240',
				 'AlAlamiya:1563:8280',
				 'SAGRINSURANCE:1423:8180',
				 'AlAhlia:1367:8140',
				 'AlRajhiTakaful:1493:8230',
				 'ALAHLITAKAFUL:1353:8130',
				 'AlinmaTokioM:1633:8312',
				 'JaziraTakaful:1185:8012',
				 'ALLIANZSF:1227:8040',
				 'ACIG:1381:8150',
				 'AmanaInsurance:1605:8310',
				 'AICC:1395:8160',
				 'ARABIANSHIELD:1269:8070',
				 'AXACooperative:1521:8250',
				 'BUPAARABIA:1465:8210',
				 'Buruj:1549:8270',
				 'GulfGeneral:1535:8260',
				 'GULFUNION:1339:8120',
				 'MALATH:1199:8020',
				 'ANBInsurance:1171:8011',
				 'SABBTAKAFUL:1283:8080',
				 'SALAMA:1241:8050',
				 'SANAD:1297:8090',
				 'SAICO:1311:8100',
				 'Enaya:1619:8311',
				 'WAFAInsurance:1325:8110',
				 'SAUDIRE:1451:8200',
				 'WALAAINSURANCE:1255:8060',
				 'Solidarity:1577:8290',
				 'TAWUNIYA:1157:8010',
				 'MEDGULF:1213:8030',
				 'TRADEUNION:1409:8170',
				 'UCA:1437:8190',
				 'Wataniya:1591:8300',
				 'WEQAYATAKAFUL:1479:8220']

	invest = ['AADC:1677:2140',
			  'ABDICO:1719:4130',
			  'ATTMCO:1705:4080',
			  'KINGDOM:1733:4280',
			  'SAICO:1663:2120',
			  'SARCO:1649:2030',
			  'SISCO:1691:2190']

	indust = ['SHAKER:1819:1214',
			  'AlSorayai:1805:1213',
			  'ALABDULLATIF:1917:2340',
			  'ASTRA:1791:1212',
			  'BCI:1763:1210',
			  'FIPCO:1861:2180',
			  'NMMCC:1875:2220',
			  'MAADEN:1777:1211',
			  'SCCO:1889:2230',
			  'SIECO:1931:4140',
			  'SPM:1903:2300',
			  'SPIMACO:1833:2070',
			  'Takween:1749:1201',
			  'ZOUJAJ:1847:2150']

	build = ['ALKHODARI:2003:1330',
		     'ALBABTAIN:2115:2320',
		     'APCO:2087:2200',
		     'Bawan:1961:1302',
		     'MESC:2143:2370',
		     'MMG:1975:1310',
		     'NGCO:2031:2090',
		     'REDSEAHOUSING:2157:4230',
		     'SAAC:2073:2160',
		     'SCACO:2045:2110',
		     'SCERCO:2017:2040',
		     'SIDC:2059:2130',
		     'SSP:1989:1320',
		     'SVCP:2129:2360',
		     'ASLAK:1947:1301',
		     'ZIIC:2101:2240']

	estate = ['ADCO:2215:4150',
			  'DARALARKAN:2257:4300',
			  'EMAAR:2229:4220',
			  'JABALOMAR:2243:4250',
			  'KEC:2271:4310',
			  'MCDCO:2201:4100',
			  'SRECO:2173:4020',
			  'TIRECO:2187:4090']

	transport = ['SAPTCO:2301:4040',
				 'SLTCO:2315:4110',
				 'Bahri:2287:4030',
				 'BUDGETSAUDI:2329:4260']

	media = ['SPPC:2373:4270',
			 'RESEARCH:2359:4210',
			 'TAPRCO:2345:4070']

	hotel = ['AlHokairGroup:2403:1820',
			 'ALTAYYAR:2389:1810',
			 'SHARCO:2417:4010',
			 'TECO:2431:4170']

	
	All = banks + petro + cement + retail + energy + agri_food + tele + insurance + invest + indust + build + estate + transport + media + hotel
	sectors = defaultdict(lambda: All, {'Banks': banks, 'Petro': petro, 'Cement': cement, 'Retail': retail,
										'Energy':energy, 'Agri_Food': agri_food, 'Tele': tele, 'Insurance': insurance,
										'Invest': invest, 'Indust': indust, 'Build': build, 'Estate': estate,
										'Transport': transport, 'Media': media, 'Hotel': hotel, 'All': All})

	option = sectors[sector]
	return option

def GetList(sector):

	humanList = []
	for entity in TadawulStocks(sector):
			x = entity.split(':')
			name = x[0]
			code = x[2]
			humanList.append(name+' '+code)
			#return name, code
	return humanList
	
def GetData(code, sector):
	'''
	sector must be a list
	'''
	for entity in sector:
		if code in entity:
			x = entity.split(':')
			name = x[0]
			number = x[1]
			code = x[2]

			return name, number, code

def GetCodes(sector):
	code_list = []
	for i in GetList(sector):
		code_list.append(i.split()[1])
	return code_list

#GetList('Banks')
#stocks('Banks')
#GetData('4170', stocks('Al'))
