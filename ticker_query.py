from config import *
import urllib.parse
import requests
import json


def get_ticker_yahoo(equity):
    response = requests.get(YAHOO_ENDPOINT.format(equity)).text
    response = response[42:-2]
    response = json.loads(response)
    try:
        return response['ResultSet']['Result'][0]['symbol']
    except:
        return None
        

def get_ticker_kensho(equity):
    response = requests.get(KENSHO_GRAPH_API['ENDPOINT'] + equity,
                            headers={'Authorization': KENSHO_GRAPH_API['TOKEN']}).json()
    try:
        results = response["data"]
        if len(results) != 0:
            for item in results:
                if not any(char.isdigit() for char in item["ticker_name"]):
                    return item["ticker_name"]
        return None
    except:
        return None
        

if __name__ == '__main__':
    print(get_ticker_yahoo('Apple'))
    print(get_ticker_yahoo("Mcdonalds"))
    print(get_ticker_kensho("Mcdonald's"))