# Amazon Price Tracker

import requests
from bs4 import BeautifulSoup
from smtplib import SMTP

# URl of the product
# URL of amazon
URL = "https://www.amazon.in/Apple-iPhone-128GB-Product-RED/dp/B0BDJVSDMY/ref=sr_1_1_sspa?crid=3ICUDBXBA3T7T&keywords=iphone+14&qid=1679603851&sprefix=iphoe+12+m%2Caps%2C4963&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"
# URL of Flipkart
# URL = "https://www.flipkart.com/apple-iphone-14-starlight-128-gb/p/itm3485a56f6e676?pid=MOBGHWFHABH3G73H&lid=LSTMOBGHWFHABH3G73HVXY5AV&marketplace=FLIPKART&q=iPhone+14&store=tyy%2F4io&srno=s_1_1&otracker=search&otracker1=search&fm=organic&iid=40268296-dc19-45b8-8eeb-6c296c311626.MOBGHWFHABH3G73H.SEARCH&ppt=pp&ppn=pp&ssid=w1s1futyxguth9mo1679833517109&qH=d36118758fc7c034"

# Set your desired price threshold for the product
Desired_PRICE = 95000

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}


# Function to check the price
def check_price():
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    # using a class that's unique to the page
    if 'amazon' in URL:
        price = soup.find("span", {"class": "a-price-whole"}).get_text().replace(',', '').replace('₹', '').strip()
    elif 'flipkart' in URL:
        price = soup.find("div", {"class": "_30jeq3 _16Jk6d"}).get_text().replace(',', '').replace('₹', '').strip()

    price = int(float(price))  # Convert the price to an integer
    return price


SMTP_SERVER = "smtp.gmail.com"
PORT = 587
EMAIL_ID = "codebytanay@gmail.com" # This is the Sender's Email_ID
PASSWORD = "daixcczrbkjhdkqo"  # This is the app generated password


# Function to send email notification
def notify():
    server = SMTP(SMTP_SERVER, PORT)
    server.starttls()
    server.login(EMAIL_ID, PASSWORD)

    subject = "BUY NOW!!"
    body = "Price has fallen. Go buy it now - " + URL
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(EMAIL_ID, "tanayt2y@gmail.com", msg)
    server.quit()


# Condition to send mail
if check_price() < Desired_PRICE:
    notify()
