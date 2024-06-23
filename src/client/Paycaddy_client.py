import os
from dotenv import load_dotenv
import requests

load_dotenv()
PAYCADDY_API_KEY = os.getenv('PAYCADDY_APY_KEY')
BASE_URL = os.getenv('BASE_URL')


def make_request(method, endpoint, data=None, params=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "X-API-KEY": PAYCADDY_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, params=params)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == 'PUT':
            response = requests.put(url, json=data, headers=headers)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, json=data, headers=headers)
        else:
            return {"error": "Invalid HTTP method"}

        response.raise_for_status()  # Lanzará una excepción para códigos de estado HTTP 4xx/5xx
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"error": "HTTP error occurred", "details": response.json(), "status_code": response.status_code}
    except requests.exceptions.RequestException as req_err:
        return {"error": "Request exception occurred", "details": str(req_err)}


def create_user_paycaddy(data):  # EndUser POST
    return make_request('POST', '/endUsers', data)


def get_user_paycaddy(user_id):  # EndUser GET
    return make_request('GET', f'/endUsers/{user_id}')


def create_wallet_credit_pc(data):  # Wallet Credit POST
    return make_request('POST', '/walletCredits', data)


def create_card_credit_pc(data):  # Credit card POST
    return make_request('POST', '/CreditCards', data)


def get_credit_card_pc(card_id):  # EndUser GET
    return make_request('GET', f'/endUsers/{card_id}')


def create_payin(data):  # payin POST
    return make_request('POST', '/payIns', data)


def get_payin(transaction_id):  # payin GET
    return make_request('GET', f'/payIns{transaction_id}')


def create_payout(data):  # payout POST
    return make_request('POST', '/payOuts', data)


def get_payouts(transaction_id):  # payout GET
    return make_request('GET', f'/payOuts{transaction_id}')
