
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 13:30:53 2016

Website: USDA-CRIS scraper, http://portal.nifa.usda.gov/web/crisprojectpages/ + links 

@author: Paul Sirma
"""


import mechanize
import sys, re, random
import os,csv
from StringIO import StringIO
from urllib2 import HTTPError
import cookielib,time
import pandas as pd 
import urllib2
from splinter.browser import Browser
from subprocess import call


import socket
#timeout in seconds see http://docs.python.org/library/socket.html#socket.setdefaulttimeout
socket.setdefaulttimeout(50000) 
 
 
url = "http://portal.nifa.usda.gov/web/crisprojectpages/"
br = mechanize.Browser()
br.set_handle_robots(False)  # bypass robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Firefox')]  # Some websites demand a user-agent that isn't a robot

  
 # Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
 
# regex to clean all 'bad' elements from strings
# str999 = re.compile('\n|\t|\r|\f|&.*?;|<.*?>|</.*?>|^[\W_]+|[\W_]+$')     #<.*?>|
str888 = re.compile('[\n\t\r\f]+|<.*?>|&.*?;', re.DOTALL)
str888ext = re.compile('[\n\t\r\f]+|<.*?>|^[\W_]+|[\W_]+$|&.*?;', re.DOTALL)
str000 = re.compile('<select.*?>.*?</select.*?>|<script.*?>.*?</script.*?>|{.*}|<noscript>.*?</noscript>', re.DOTALL)
strand = re.compile('&amp;')        
       
path = 'C:\Users\psirma\Desktop\Personal.Projects\python\usda_scraper'.replace("\\" , "/")
# links = open('g:/usda_data/cris/project_html_links.txt').read().split('\n')
links = csv.reader(file(path+'/project_html_links_v2.csv','rb'))

# proxy_handler = urllib2.ProxyHandler({})
# opener = urllib2.build_opener(proxy_handler)
# urllib2.install_opener(opener)

#Output 
outp = csv.writer(open(path+'/main_info_USDA_awards_ps.csv','ab'))

outcomereports = csv.writer(open(path+'/progress_reports_USDA_awards_ps.csv','ab'))
 
mainheader = ['Project Title', 'Sponsoring Institution', 'Project Status', 'Funding Source', 'Reporting Frequency', 'Accession No.', 'Grant No.', 'Project No.', 'Proposal No.', 'Multistate No.', 'Program Code', 'Project Start Date', 'Project End Date', 'Project Director', 'Recepient Organization', 'Organization Street', 'Organization Address', 'Performing Department', 'Non-Technical Summary', 'Animal Health Component', 'Basic', 'Applied', 'Developmental', 'Knowledge Area', 'Subject Of Investigation', 'Field Of Science', 'Keywords', 'Goals / Objectives', 'Project Methods','URL']
 #outp.writerow(mainheader)
 
outheader = ['Award Number','Period Start Date','Period End Date','Outputs','Impacts','Publications']
# outcomereports.writerow(outheader) 



for numb in links:
	l = numb[0]
	print url+l
	row = []
	mainrow = []
	awardnum = re.search('^\d+',l).group()
	browser = Browser()
	browser.visit(url+l)

	#Project title
	title = browser.find_by_css('#title b')
	for t in title:
		row.append(t.text.encode('utf8'))
        mainrow.append('Project Title')

    #Basic information on award
	basicinfo = browser.find_by_css('.second')
	for b in basicinfo:
		# print b.text 
		one = b.find_by_css('div')
		for n in range(1,len(one)-5,5):
			# row.extend([str888.sub('',one[n].text.encode('utf8')),str888.sub('',one[n+2].text.encode('utf8'))])
			# mainrow.extend([str888.sub('',one[n+1].text.encode('utf8')),str888.sub('',one[n+3].text.encode('utf8'))])

			row.extend([str888.sub('',one[n].text),str888.sub('',one[n+2].text)])
			mainrow.extend([str888.sub('',one[n-1].text),str888.sub('',one[n+1].text)])
		# print row 
		# print mainrow

		#Project Director 
		projectdir = browser.find_by_css('#project_director_div a')
		for p in projectdir:
			mainrow.append('Project Director')
			row.append(str888.sub('',p.text.encode('utf8')))
		#Info on recepient organization 
		recipientorg = browser.find_by_css('#recipient_org_div')
		for r in recipientorg :
			name = r.find_by_css('.leftcol')
			for n in name :
				mainrow.extend(['Recepient Organization','Organization Street','Organization Address'])
				nama = n.find_by_css('a')
				row.append( nama[0].text.encode('utf8'))
				namaddress = n.text.encode('utf8').split("\n")  #splitting my new line
				street = str888.sub('',namaddress[2])
				city = str888.sub('',namaddress[3])
				row.extend([street,city])
				dept = r.find_by_css('.rightcol')
				for d in dept:
					mainrow.append('Performing Department')
					depart = d.text.encode('utf8').split("\n")
					depname = strand.sub('and',depart[1])
					depname = str888.sub('',depname)
					row.append(depname)
				#Additional info including keywords, research effort, knowledge areas, etc.
				otherinfo = browser.find_by_css('.padding-left-10')

				#Non-technical summary 
				abstr = otherinfo[0].text.encode('utf8').split("\n")
				summary = str888ext.sub('',abstr[1])
				mainrow.append('Non-Technical Summary')
				row.append(summary)

				#Animal health component
				animhealth = otherinfo[1].find_by_css('.rightcol')[0].text.encode('utf8')
				mainrow.append('Animal Health Component')
				row.append(animhealth)

				#Research effort categories
				cat = otherinfo[1].find_by_css('.leftcol .container div')
				for n in range(0,len(cat),3):
					mainrow.append(cat[n].text.encode('utf8'))
					row.append(cat[n+1].text.encode('utf8'))

				#Classification 
				classif = otherinfo[3].text.encode('utf8').split("\n\n")
				for c in classif:
					tit = c.split("\n")
					categ = str888.sub('',tit[0])
					cont = str888ext.sub('',tit[1])
					mainrow.append(categ)
					row.append(cont)
				#Keywords
				keywords = browser.find_by_css('#keywords a')
				allkey = []
				for k in keywords :
					key = re.sub(' $','',k.text.encode('utf8')) #Removing trailling blank 
					# allkey.append(re.sub('^ ',';',key))
					allkey.append(re.sub('^ ',';',key))
				# print allkey
				mainrow.append('Keywords')
				row.append(allkey)

				# allkey = ''
		  #       for k in keywords:
		  #           key = re.sub(' $','',k.text.encode('utf8'))
		  #           allkey+=re.sub('^ ',';',key)
		  #       mainrow.append('Keywords')
		  #       row.append(allkey)

				#Goals/objectives
				goals = otherinfo[5].text.encode('utf8').split("\n")
				goaltext = str888ext.sub('',goals[1])
				mainrow.append('Goals / Objectives')
				row.append(goaltext)

				#Project MEthods
				methods = otherinfo[6].text.encode('utf8').split("\n")
				meth = str888ext.sub('',methods[1])
				mainrow.append('Project Methods')
				row.append(meth)

				#Progress Reports
				progress = browser.find_by_css('.fourth td')
				for p in progress :
					outputs = []
					maininfo = p.find_by_css('p')
					info = maininfo[0].text.encode('utf8').split("\n\n")
					dates = info[0].split("Progress")[1].split("to")
					outputs.extend([awardnum,dates[0],dates[1]])
					for nu in range(1,len(info)-1):
						need = info[nu].split("\n")
						outputs.append( str888.sub('',need[1]))
					pubs = p.find_by_css('li')
					allpubs = ''
					for pu in pubs :
						pubo = str888ext.sub(' ',pu.text.encode('utf8'))
						pubo = re.sub(' $','',pubo)
						allpubs += pubo+ "; "
					finalpubs =  re.sub('; $','',allpubs)
					outcomereports.writerow(outputs+[finalpubs])
				mainrow.append('URL')
				row.append(url+l)

				if mainrow ==mainheader :
					print "Looking good Sir"
					pass
				else :
					print "We have a problem here"
					print mainrow
					print mainheader

				outp.writerow(row)
				numbers = open(path+'/provisional_testing.txt','a')
				print >>numbers,numb
				numbers.close()
				# call("taskkill /F /IM plugin-container.exe" , shell=True)
        		browser.quit()

print "The end"





































		



