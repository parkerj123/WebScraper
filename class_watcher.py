# This program scrapes a website and prints the contents to std output

from bs4 import BeautifulSoup as bs4
import requests
import smtplib
from email.message import EmailMessage
import ssl

'''

This is a docstring example.

This program is useful when you want to search
for generic tags and scrape them from a website.
'''

def send_email_to_me():
    sender = "parkerjanke1@gmail.com"
    reciever = "7605199806@vtext.com"
    msg = """
    Check UNLV, a class is open!
    """

    port = 465
    password = "James1997!"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("parkerjanke1@gmail.com", password)
        server.sendmail(sender,reciever,msg)

email = False

session = requests.Session()
payload = {'userid': '5007233759',
           'pwd': 'Flute1997!'}

s = session.post("https://my.unlv.nevada.edu/psp/lvporprd/?cmd=login&languageCd=ENG",
                 data=payload)
s = session.get("https://my.unlv.nevada.edu/psc/lvporprd_newwin/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_SHOP_CART_FL.GBL?Page=SSR_TERM_STA3_FL&amp;pslnkid=ADMN_S202002190709346968291268")


# Get URL data
soup = bs4(s.text, features="html.parser")
elem = soup.find_all('span')

for x in elem:
    if x.get('id'):
        if x.get('id').find("DERIVED_SSR_FL_SSR_AVAIL_FL$") != -1:
            if (x.text) != "Closed":
                email = True

if email:
    send_email_to_me()
