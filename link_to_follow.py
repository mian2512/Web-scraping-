
"""
Created on Tue Apr 30 21:26:53 2013

Website: USDA-CRIS scraper, http://portal.nifa.usda.gov/web/crisprojectpages/

@author: Paul Sirma 
"""

#Packages needed to run this code
import mechanize
import splinter
import ssl
import pandas as pd
import re , sys, random
from urllib2 import HTTPError
from time import sleep
from subprocess import call
from splinter.browser import Browser
import os.path, re, sys, random, csv


path = 'C:\Users\psirma\Desktop\Personal.Projects\python\usda_scraper'.replace("\\" , "/")


import mechanize,cookielib

br = mechanize.Browser()
br.set_handle_robots(False)  # bypass robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'chrome')]  # Some websites demand a user-agent that isn't a robot
# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
browser = Browser()
br = mechanize.Browser()

url = "http://portal.nifa.usda.gov/web/crisprojectpages/"

br.open(url)

myfiles = []
filetypes=[".html",".php"] #you will need to do some kind of pattern matching on your files



for l in br.links():
	print "Inside a loop"
	for t in filetypes:
		if t in str(l) :
			#print(link)= Link(base_url='http://portal.nifa.usda.gov/web/crisprojectpages/?C=N;O=D', url='0200940-experimental-analysis-and-modeling-of-macropore-flow-during-artificial-subsurface-drainage.html', text='0200940-experimental-analysis-and-modeling-of-macropore-flow-during-artificial-subsurface-drainage.html', tag='a', attrs=[('href', '0200940-experimental-analysis-and-modeling-of-macropore-flow-during-artificial-subsurface-drainage.html')])
			print l.url 
			link = l.url 
			myfiles.append(link)
			data = pd.DataFrame(myfiles)
			data.to_csv(path+'/project_html_links.csv')
print "done"



