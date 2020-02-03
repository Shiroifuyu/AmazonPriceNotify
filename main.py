import requests
from bs4 import BeautifulSoup
import re
import smtplib
import time

URL = "https://www.amazon.es/Lenovo-Ideapad-330-15ICH-Ordenador-GTX1050-2GB/dp/B07R2F6NR3/ref=sr_1_7?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3F9VWX7P1MLYB&keywords=portatiles&qid=1580729004&smid=A1AT7YVPFBWXBL&sprefix=portati%2Caps%2C157&sr=8-7"
headers = {"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
page = requests.get(URL, headers=headers)

def check_price():
    #Use 2 soups because Amazon generates it's pages with JavaScript
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
    title = soup2.find(id="productTitle").get_text()
    price = soup2.find(id="priceblock_dealprice").get_text()

    #Convert the price(string) into a float with regex
    regex = re.search(r'\d+,\d*', price)
    #Replace the ',' in the price to '.' so we can cast it to float
    converted_price = float(regex.group(0).replace(',', '.'))
    #Print for debugging
    print(title.strip())
    print(converted_price)

    if converted_price < 500: #Input desired price
        send_email()

def send_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('YOUR EMAIL', 'GOOGLE 2FA TO SEND THE EMAIL')

    subject = 'Price fell down'
    body = 'Amazon link: ' + URL

    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        'EMAIL FROM WHERE YOU SEND',
        'EMAIL WHO RECEIVES',
        msg
    )

    print("Email has been sent")
    server.quit()

while(True):
    check_price()
    time.sleep(60 * 60) #Check the price every minute