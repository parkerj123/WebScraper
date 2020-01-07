# This program scrapes a website and prints the contents to std output

from bs4 import BeautifulSoup as bs4
import urllib3
import certifi
import argparse
from collections import defaultdict
import csv

'''

This is a docstring example.

This program is useful when you want to search
for generic tags and scrape them from a website.
'''

parser = argparse.ArgumentParser(description="Scrape a website")
parser.add_argument('-u',
                    metavar='URL',
                    type=str,
                    help="The URL to be scraped")

parser.add_argument('-t',
                    metavar='Tag(s)',
                    nargs='*',
                    type=str,
                    help="A list of tags to include in the scrape. \
                    Defaults to all",
                    default=None)

args = parser.parse_args()

BASE_PATH = "https://census.gov"
DEFAULT_URL = "https://www.census.gov/programs-surveys/popest.html"
url = ''
tags = True

if args.u:
    url = args.u
else:
    url = DEFAULT_URL

if args.t is not None:
    tags = True

titles_formatted = defaultdict(lambda: 0)


# Used to make requests, takes care of all pooling and thread safety
lib = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                          ca_certs=certifi.where())

# Get URL data
content = lib.request('GET', url).data
soup = bs4(content, features="html.parser")
html_data = soup.find_all(args.t)
for link in html_data:
    if link.get('href') is not None:
        if link.get('href')[0] == "/":
            href = BASE_PATH + link.get('href')
            if href.endswith("/"):
                titles_formatted[href[:-1]] = 1
            else:
                titles_formatted[href] = 1
        elif link.get('href').find('#') != -1:
            if link.get('href').find('#') > 0:
                titles_formatted[link.get('href')[:link.get('href').find('#')]] = 1
        else:
            if link.get("href").endswith("/"):
                titles_formatted[link.get("href")[:-1]] = 1
            else:
                titles_formatted[link.get("href")] = 1
    else:
        continue

with open('links.csv', mode='w') as linksCSV:
    fieldNames = ['link', 'count']
    writer = csv.DictWriter(linksCSV, fieldnames=fieldNames)
    writer.writeheader()
    for k, v in titles_formatted.items():
        writer.writerow({'link': k, 'count': v})
