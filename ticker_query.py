from config import *
import urllib.parse
import requests 
import json
from yahoo_getter import cacheify

@cacheify('tickers')
def get_ticker_yahoo(equity):
		response = requests.get( YAHOO_ENDPOINT.format(equity) ).text
		response = response[42:-2]
		response = json.loads(response)
		if len(response['ResultSet']['Result']) != 0:
			return response['ResultSet']['Result'][0]['symbol']
		return None	


def get_ticker_kensho(equity):
		response = requests.get( KENSHO_GRAPH_API['ENDPOINT'] + equity, headers={'Authorization': KENSHO_GRAPH_API['TOKEN']}).json()
		results = response["data"]
		# If there is a ticker name, return it.
		if len(results) != 0 and "ticker_name" in results[0]:
			return results[0]["ticker_name"]
		return None