import time
import requests
from bs4 import BeautifulSoup
import secrets
from twilio.rest import Client
import webbrowser

url = "https://www.marukyu-koyamaen.co.jp/english/shop/products/1161020c1/"
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"}

def get_page_html(url: str, headers: dict) -> str:
    page = requests.get(url, headers=headers)
    return page.content

def check_if_item_in_stock(page_html: str) -> bool:
    soup = BeautifulSoup(page_html, 'html.parser')
    
    out_of_stock_div = soup.find_all("p", {"class": "stock out-of-stock amount-0"})
    return len(out_of_stock_div) < 5

def setup_twilio_client():
    account_sid = secrets.TWILIO_ACCOUNT_SID_TEST
    auth_token = secrets.TWILIO_AUTH_TOKEN_TEST
    return Client(account_sid, auth_token)

def send_notification(twilio_client):
    twilio_client.messages.create(
        body="Your matcha is available for purchase.",
        from_=secrets.TWILIO_FROM_NUMBER,
        to=secrets.MY_PHONE_NUMBER
    )

def open_in_stock_link():
    webbrowser.open(url, new=0, autoraise=True)
def main():

    # twilio_client = setup_twilio_client()
    while True:
        page_html = get_page_html(url, headers=headers)
        if check_if_item_in_stock(page_html):
            #send_notification(twilio_client)
            print("In stock, opening link!")
            open_in_stock_link()
            break
        else:
            print("Out of stock...")
            time.sleep(60)
    


if __name__ == "__main__":
    main()