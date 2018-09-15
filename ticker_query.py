from config import *
import urllib.parse
import requests 
import json

def get_ticker_yahoo(equity):
		response = requests.get( YAHOO_ENDPOINT.format(equity) ).text
		response = response[42:-2]
		response = json.loads(response)
		return response['ResultSet']['Result'][0]['symbol']


def get_ticker_kensho(equity):
		response = requests.get( KENSHO_GRAPH_API['ENDPOINT'] + equity, headers={'Authorization': KENSHO_GRAPH_API['TOKEN']}).json()
		results = response["data"]
		# If there is a ticker name, return it.
		if len(results) != 0 and "ticker_name" in results[0]:
			return best_result["ticker_name"]
		return None
# format YAHOO_ENDPOINT with url-encoded string that we want to search for
# gives back some json, get the first result.

get_ticker_yahoo('Apple')