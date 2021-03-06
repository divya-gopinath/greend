import plaid
from config import *
from flask import Flask, render_template, request, send_file, make_response, send_from_directory, jsonify
import datetime
import requests
from ticker_query import *
from markov_filter import *


class Greend(object):
	app = None

	def __init__(self):
		self.app = Flask(__name__)
		self.app.add_url_rule('/', view_func=self.render_html)
		self.app.add_url_rule("/get_access_token", view_func=self.get_access_token, methods=['POST'])
		self.app.add_url_rule("/accounts", view_func=self.accounts, methods=['GET'])
		self.app.add_url_rule("/transactions", view_func=self.transactions, methods=['GET', 'POST'])
		self.app.add_url_rule("/create_public_token", view_func=self.create_public_token, methods=['GET'])

		self.access_token = None
		self.public_token = None
		self.transaction_data = None
		self.client = plaid.Client(PLAID_CLIENT['PLAID_CLIENT_ID'],
								   PLAID_CLIENT['PLAID_SECRET'],
								   PLAID_CLIENT['PLAID_PUBLIC_KEY'],
								   PLAID_CLIENT['PLAID_ENV'])

	def run(self):
		self.app.run()

	def render_html(self):
		return render_template('index.ejs',
							   plaid_public_key=PLAID_CLIENT['PLAID_PUBLIC_KEY'],
							   plaid_environment=PLAID_CLIENT['PLAID_ENV'])

	def get_access_token(self):
		self.public_token = request.form['public_token']
		exchange_response = self.client.Item.public_token.exchange(self.public_token)
		print('access token: ' + exchange_response['access_token'])
		print('item ID: ' + exchange_response['item_id'])
		self.access_token = exchange_response['access_token']
		print("WWOWOWOWO! " + str(self.access_token))
		return jsonify(exchange_response)

	def accounts(self):
		accounts = self.client.Auth.get(self.access_token)
		return jsonify(accounts)

	def item(self):
		item_response = self.client.Item.get(self.access_token)
		institution_response = self.client.Institutions.get_by_id(item_response['item']['institution_id'])
		return jsonify({'item': item_response['item'], 'institution': institution_response['institution']})

	def transactions(self):
		# Pull transactions for the last 30 days
		start_date = "{:%Y-%m-%d}".format(datetime.datetime.now() + datetime.timedelta(-TRANSACTION_WINDOW))
		end_date = "{:%Y-%m-%d}".format(datetime.datetime.now())

		try:
			response = self.client.Transactions.get(self.access_token, start_date, end_date)
			self.transaction_data = response
			self.get_tickers()
			return jsonify(response)
		except plaid.errors.PlaidError as e:
			return jsonify({'error': {'error_code': e.code, 'error_message': str(e)}})

	def create_public_token(self):
		# Create a one-time use public_token for the Item. This public_token can be used to
		# initialize Link in update mode for the user.
		response = self.client.Item.public_token.create(self.access_token)
		return jsonify(response)

	def get_tickers(self):
		# called when self.transaction_data has data to work with; want to iterate
		# and call get_ticker for each one
		#print(self.transaction_data['transactions'])
		transactions = []
		desired_properties = ['name', 'amount']
		for transaction in self.transaction_data['transactions']:
		    tr = {}
		    for property in desired_properties:
		        tr[property] = transaction[property]
		    if 'name' in desired_properties:
		        ticker_kensho = get_ticker_kensho(clean(tr['name']))
		        if ticker_kensho is not None:
		            tr['name'] = ticker_kensho
		        else:
		            tr['name'] = get_ticker_yahoo(clean(tr['name']))
		    transactions.append(tr)
		print(transactions)
		return transactions
		

	def get_ticker_kensho(self, equity):
		response = requests.get( KENSHO_GRAPH_API['ENDPOINT'] + equity, headers={'Authorization': KENSHO_GRAPH_API['TOKEN']}).json()
		results = response["data"]
		# If there is a ticker name, return it.
		if len(results) != 0 and "ticker_name" in results[0]:
			return best_result["ticker_name"]
		return None
			
if __name__ == '__main__':
	Greend().run()
