# Amazon Price Tracker

import requests
from bs4 import BeautifulSoup
from smtplib import SMTP
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        url = request.form['url']
        user_email = request.form['email']
        desired_price = int(request.form['price'])

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }

        # Function to check the price
        def check_price():
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            # using a class that's unique to the page
            if 'amazon' in url:
                price = soup.find("span", {"class": "a-price-whole"}).get_text().replace(',', '').replace('₹',
                                                                                                          '').strip()
            elif 'flipkart' in url:
                price = soup.find("div", {"class": "_30jeq3 _16Jk6d"}).get_text().replace(',', '').replace('₹',
                                                                                                           '').strip()

            price = int(float(price))  # Convert the price to an integer
            return price

        # SMTP_SERVER = "smtp.gmail.com"
        smtp_server = "smtp.gmail.com"
        # PORT = 587
        port = 587
        # EMAIL_ID = "codebytanay@gmail.com"  # This is the Sender's Email_ID
        email_id = "codebytanay@gmail.com"
        # PASSWORD = "daixcczrbkjhdkqo"  # This is the app generated password
        password = "daixcczrbkjhdkqo"

        # Function to send email notification
        def notify():
            server = SMTP(smtp_server, port)
            server.starttls()
            server.login(email_id, password)

            subject = "BUY NOW!!"
            body = "Price has fallen. Go buy it now - " + url
            msg = f"Subject: {subject}\n\n{body}"

            server.sendmail(email_id, user_email, msg)
            server.quit()

        # Condition to send mail
        if check_price() < desired_price:
            notify()

        return render_template('ans.html')


app.run(debug=True)
