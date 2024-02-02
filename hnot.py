from bs4 import BeautifulSoup
import requests
import io
import sys
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

bot_token = ''
chat_id = ''

response = requests.get('https://jiji.com.et/cars?price_min=1500000&price_max=3000000')
soup = BeautifulSoup(response.text, 'html.parser')
cars = soup.find_all('div', class_='b-advert-title-inner qa-advert-title b-advert-title-inner--div')
description = soup.find_all('div', class_='b-list-advert-base__description-text')
links = soup.find_all('div', class_='b-list-advert__gallery__item js-advert-list-item')

def send_to_telegram(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, params=params)
    return response.json()

for index, entry in enumerate(cars):
    title = entry.get_text(strip=True)
    des = description[index].get_text(strip=True)
    
    # Extract the link for each car entry
    link = links[index].find('a', href=True)['href']
    
    texts = f"Car Name: {title}\nDescription: {des}\nLink: https://jiji.com.et{link}\n"
    response = send_to_telegram(bot_token, chat_id, texts)
    print(response)
    time.sleep(30)
