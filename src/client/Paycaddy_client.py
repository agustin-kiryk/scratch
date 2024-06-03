import os

from dotenv import load_dotenv
import requests

load_dotenv()
PAYCADDY_API_KEY = os.getenv('PAYCADDY_APY_KEY')
BASE_URL = os.getenv('BASE_URL')


def make_request(method, endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "X-API-KEY": PAYCADDY_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        if method.upper() == 'GET':
            response = requests.get(url, json=data, headers=headers)
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


def create_user_paycaddy(data):  #EndUser POST
    return make_request('POST', '/endUsers', data);


def get_user_paycaddy(data):  #EndUser GET
    return make_request('GET', '/endUsers', data);
