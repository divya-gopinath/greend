from config import *
import urllib.parse
import requests
import json


def get_ticker_yahoo(equity):
    response = requests.get(YAHOO_ENDPOINT.format(equity)).text
    response = response[42:-2]
    response = json.loads(response)
    return response['ResultSet']['Result'][0]['symbol']


def get_ticker_kensho(equity):
    response = requests.get(KENSHO_GRAPH_API['ENDPOINT'] + equity,
                            headers={'Authorization': KENSHO_GRAPH_API['TOKEN']}).json()
    results = response["data"]
    if len(results) != 0 and "ticker_name" in results[0]:
        return results[0]["ticker_name"]
    return None


if __name__ == '__main__':
    get_ticker_yahoo('Apple')
