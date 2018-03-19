#!/usr/bin/env python
# coding=utf-8

from flask import Flask
from flask import render_template
from flask import request
import braintree

import os, json, random

app = Flask(__name__)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'secrets.json')) as data_file:    
	secret = json.load(data_file)
gateway = braintree.BraintreeGateway(access_token=secret['access_token'])

@app.route('/')
def index():
	print('Hello World!')
	return 'Hello, World!'

@app.route('/test')
def test():
	return render_template('test.html')

@app.route('/hello_world')
def hello_world():
	return render_template('hello_world.html')

@app.route("/client_token", methods=["GET"])
def client_token():
	return gateway.client_token.generate()

@app.route('/sandbox')
def paypal_checkout():
	# client_token = gateway.client_token.generate()
	# return render_template('sandbox.html', client_token=client_token)
	return render_template('sandbox.html')

@app.route("/checkout", methods=["POST"])
def create_purchase():
	nonce = request.form["nonce"]
	print('nonce: ' + str(nonce))
	# Use payment method nonce here...
	result = gateway.transaction.sale({
		"amount" : request.form["amount"],
		# "amount" : '1.13',
		"merchant_account_id": "USD",
		# "payment_method_nonce" : request.form["payment_method_nonce"],
		"payment_method_nonce" : nonce,
		"order_id" : "test1313" + str(random.randint(1, 99999)),
		"descriptor": {
			"name": "abc*foo.com"
		},
		"shipping": {
			"first_name": "Jen",
			"last_name": "Smith",
			"company": "Braintree",
			"street_address": "1 E 1st St",
			"extended_address": "Suite 403",
			"locality": "Bartlett",
			"region": "IL",
			"postal_code": "60103",
			"country_code_alpha2": "US"
		},
		"options" : {
			"paypal" : {
				"custom_field" : "PayPal custom field",
				"description" : "Description for PayPal email receipt"
			}
		}
	})
	mes = ''
	if result.is_success:
		mes = "Success ID: ".format(result.transaction.id)
	else:
		mes = format(result.message)
	return mes

if __name__ == "__main__":
	app.run()