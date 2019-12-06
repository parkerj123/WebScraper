#This program scrapes a website and prints the contents to std output

from bs4 import BeautifulSoup as bs4
import urllib3
import certifi
import os,sys
import argparse
from collections import defaultdict
import csv 


parser = argparse.ArgumentParser(description="Scrape a website")
parser.add_argument('-u', 
		    metavar='URL', 
		    type=str, 
		    help="The URL to be scraped")
parser.add_argument('-t', 
		    metavar='Tag(s)', 
		    nargs='*', 
		    type=str, 
		    help="A list of tags to include in the scrape. Defaults to all", 
		    default=None)

args= parser.parse_args()

DEFAULT_URL = "www.hostedgraphite.com"
url = ''
tags = True

if args.u:
	url = args.u
else:
	url = DEFAULT_URL

if args.t is None:
	tags = False

titles_raw = []
titles_formatted = defaultdict(lambda :0)



# Used to make requests, takes care of all pooling and thread safety
lib = urllib3.PoolManager(
			cert_reqs='CERT_REQUIRED',
			ca_certs=certifi.where())

# Get URL data
content = lib.request('GET',url).data

soup = bs4(content,features="html.parser")

#print(soup.prettify())

#print(soup.title.string)

#print(soup.a.get('class'))

#for link in soup.find_all('a'):
#	print(link.get('href'))

#print(soup.body.get_text())


# if tags == True:
# 	for lines in soup.find_all(args.t):
# 		print(lines)
# else:
# 	print(soup.prettify())
bad_rex = ['!','@','#','$','%','^','&','*','+','=','{','}','|','[',']','\\',';','\"',':','\'','(',')']


stuff = soup.find_all('div')
for s in stuff:
	#print(s.get('class'))
	if (s.get('class') != None) and (s.get('class')[0] == "blog-title-2"):
		#print(s.string)
		titles_raw.append(s.string)
	#else:
	#	print('Not this one')

#print(titles_raw)

for titles in titles_raw:
	break_it = False
	title = titles.lower().split()
	for new_title in title:
		for char in new_title:
			if char in bad_rex:
				i = new_title.find(char)
				new_title = new_title[0:i]
				titles_formatted[new_title]+=1
				break_it = True
				break;
		titles_formatted[new_title]+=1



#for keys in titles_formatted.keys():
#	print(keys)

with open('scrapper.csv', mode='w') as scraperCSV:
	fieldNames = ['word', 'count']
	writer = csv.DictWriter(scraperCSV, fieldnames=fieldNames)
	writer.writeheader()

	for k, v in titles_formatted.items():
		writer.writerow({'word': k, 'count': v})




