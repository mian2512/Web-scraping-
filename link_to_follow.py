
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
path2 = 'C:\Users\psirma\Desktop\Personal.Projects\python\usda_scraper\links_to_follow'.replace("\\" , "/")


import mechanize,cookielib

br = mechanize.Browser()
# br.set_handle_robots(False)  # bypass robots
# br.set_handle_refresh(False)  # can sometimes hang without this
# br.addheaders = [('User-agent', 'chrome')]  # Some websites demand a user-agent that isn't a robot

# # Cookie Jar
# cj = cookielib.LWPCookieJar()
# br.set_cookiejar(cj)
browser = Browser()

br = mechanize.Browser()

url = "http://portal.nifa.usda.gov/web/crisprojectpages/"
#Open the url 
# open_browser = browser.visit(url)
# sleep(1)

# link = browser.find_by_css('td')
# print link 

# l = "0001176-plant-genetic-resources-conservation-and-utilization.html"


# response = br.open(url+l)
# resp2 = response.get_data()

# http://portal.nifa.usda.gov/web/crisprojectpages/0001176-plant-genetic-resources-conservation-and-utilization.html
# http://portal.nifa.usda.gov/web/crisprojectpages/0001176-plant-genetic-resources-conservation-and-utilization.html

br.open(url)
myfiles = []
filetypes=[".html",".php"] #you will need to do some kind of pattern matching on your files
# br.follow_link(text_regex=r"\.html\.php"):



for l in br.links():
	print "Inside a loop"
	for t in filetypes:
		if t in str(l) :
			print "I am here "
			print l.url 
			link = l.url 
			myfiles.append(link)
			data = pd.DataFrame(myfiles)
			data.to_csv(path+'/project_html_links.csv')
print "done"



# def downloadlink(l):
#     f=open(l.text,"w") #perhaps you should ensure that file doesn't already exist.

#     br.click_link(l)
#     f.write(br.response().read())
#     print l.text," has been downloaded"
#     #br.back()

# for l in myfiles:
#     sleep(1) #throttle so you dont hammer the site
#     downloadlink(l)




# print "The response is: %s" %open_browser

# # links = br.follow_link()

# Links = []
# for link in br.links():
# 	req = br.click_link(link)
# 	br.open(req)
# 	br.back()






#Define a function to retrive and save all of the links under the website 
# links = []
# def retrive_links(url):
	# """
	# This function retrive all the links in a given url 
	# *******
	# Parameters:
	# 	url: http://portal.nifa.usda.gov/web/crisprojectpages/
	# 	this is where the data is 
	# *******
	# Output:
	# 	link: a txt file 
	# """
	# links = br.follow_link()

# Link(base_url='http://portal.nifa.usda.gov/web/crisprojectpages/?C=N;O=D', url='0200940-experimental-analysis-and-modeling-of-macropore-flow-during-artificial-subsurface-drainage.html', text='0200940-experimental-analysis-and-modeling-of-macropore-flow-during-artificial-subsurface-drainage.html', tag='a', attrs=[('href', '0200940-experimental-analysis-and-modeling-of-macropore-flow-during-artificial-subsurface-drainage.html')])
