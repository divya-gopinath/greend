import numpy as np
from flask import Flask, render_template, request, send_file, make_response, send_from_directory, jsonify

class Greend(object):
	app = None

	def __init__(self):
		self.app = Flask(__name__)
		self.app.add_url_rule('/', view_func=self.render_html)
		
	def run(self):
	    self.app.run()

	def render_html(self):
	    return render_template('index.html')

		
if __name__ == '__main__':
    Greend().run()