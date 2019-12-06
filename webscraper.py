from bs4 import BeautifulSoup as bs4
import urllib3
import certifi
import os,sys
import argparse 


parser = argparse.ArgumentParser(description="Scrape a website")
parser.add_argument('-u', metavar='URL', type=str, help="The URL to be scraped")
parser.add_argument('-t', metavar='Tag(s)', nargs='*', type=str, help="A list of tags to include in the scrape. Defaults to all", default=None)
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


if tags == True:
	for lines in soup.find_all(args.t):
		print("%s -- class: %s" % (lines.name, lines.get('class')))
else:
	print(soup.prettify())

