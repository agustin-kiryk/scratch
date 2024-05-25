import os

from dotenv import load_dotenv
import requests

load_dotenv()
PAYCADDY_APY_KEY = os.getenv('PAYCADDY_APY_KEY')
BASE_URL = os.getenv('BASE_URL')

def create_user(data):
    url = f"{BASE_URL}/endUsers"
    headers = {
        "X-API-KEY": PAYCADDY_APY_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

