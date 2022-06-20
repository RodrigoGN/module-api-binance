from urllib.parse import urlencode
from dotenv import load_dotenv
from requests import get, post
import hashlib
import hmac
import os
load_dotenv()
api_url = os.getenv("URL_API") if os.getenv("TEST") == "False" else os.getenv("URL_TEST")
api_key = os.getenv("BINANCE_API_KEY") if os.getenv("TEST") == "False" else os.getenv("BINANCE_API_KEY_TESTE")
secret_key = os.getenv("BINANCE_SECRETKEY") if os.getenv("TEST") == "False" else os.getenv("BINANCE_SECRETKEY_TEST")


def private_call(path, data=None, method='GET') -> dict or str:
    if not api_key or not secret_key:
        raise Exception('API key e secret key nao configurados')
    recv_window = 60000
    timestamp = get(f'{api_url}/v3/time').json()["serverTime"]
    msg_sig = {}
    if data:
        for i in data:
            msg_sig[f'{i}'] = data[f'{i}']
    msg_sig["timestamp"] = timestamp
    msg_sig["recvWindow"] = recv_window
    signature = hmac.new(secret_key.encode('utf-8'), str(urlencode(msg_sig)).encode('utf-8'), hashlib.sha256)\
        .hexdigest()
    new_data = {}
    if data:
        for i in data:
            new_data[f'{i}'] = data[f'{i}']
    new_data["timestamp"] = timestamp
    new_data["recvWindow"] = recv_window
    new_data["signature"] = signature
    req_met = get if method == "GET" else post
    try:
        result = req_met(url=f'{api_url}{path}', params=new_data, headers={'X-MBX-APIKEY': api_key})
        return result.json()
    except Exception as e:
        print("Voce recebeu o erro: " + str(e))
        return str(e)


def account_info():
    return private_call('/v3/account')


def new_order(symbol, quantity, price=False, side='BUY',  tipo='MARKET', time_in_force='GTC') -> dict:
    data = {"symbol": symbol, "side": side, "type": tipo, "quantity": quantity}
    if price:
        data["price"] = price
    if type == 'LIMIT':
        data["timeInForce"] = time_in_force
    return private_call('/v3/order', data, 'POST')


def public_call(path, data=None, m='GET'):
    try:
        qs = f"?{urlencode(data)}" if data else ""
        url = f'{api_url}{path}{qs}'
        req_met = get if m == "GET" else post
        result = req_met(str(url))
        return result.json()
    except Exception as e:
        print("Voce recebeu o erro: " + str(e))
        return str(e)


def time():
    return public_call(f'/v3/time')


def coin_price(symbol) -> dict:
    return public_call('/v3/ticker/price', {"symbol": symbol})


def depht(symbol='BTCUSDT', limit=5):
    return public_call('/v3/depth', {"symbol": symbol, "limit": limit})


def exchange_info():
    return public_call('/v3/exchangeInfo')

if __name__ == "__main__":
    print(coin_price("BTCUSDT")["price"])
    #print(account_info()['balances'])
    #print(new_order("BTCUSDT", 0.00030))
    #print(new_order("BTCUSDT", 0.00030, side="SELL"))