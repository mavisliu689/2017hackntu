from flask import Flask, render_template, request, jsonify
import os
import json
import urllib
import requests

app = Flask(__name__)

port = int(os.getenv('PORT', 8000))

# class CustomFlask(Flask):
#     jinja_options = Flask.jinja_options.copy()
#     jinja_options.update(dict(
#       block_start_string='{%',
#       block_end_string='%}',
#       variable_start_string='((',
#       variable_end_string='))',
#       comment_start_string='{#',
#       comment_end_string='#}',
#     ))


# app = CustomFlask(__name__)
@app.route('/test')
def test():
    return render_template('index.html')


@app.route('/')
def question():
    return render_template('question.html')

@app.route('/list_r')
def list_r():
    return render_template('list.html')

@app.route('/profile')
def profile():
	stock_info = get_stock_api()
	return render_template('profile.html')

def get_stock_api():

    stock_api_url = 'http://54.65.120.143:8888/hackathon/eSTKList'
    data = {
		"StockID":"2845"
	}
    response = requests.post(stock_api_url, json=data)
    stock_info = response.text
    response_text=x.replace('\n', '')
	response_text=x.replace(' ', '')
    return stock_info

from datetime import datetime
import socket
def new_order(**kwargs):
    AcctID = kwargs.get('AcctID', 'B299491384')
    CustID = kwargs.get('CustID', 'B299491384')
    ClientIP = kwargs.get('CustID', socket.gethostbyname(socket.gethostname()))
    TranDate = kwargs.get('TranDate', datetime.now().strftime("%Y%m%d"))
    BS = kwargs.get('BS', 'B') #買進賣出
    StockID = kwargs.get('StockID', '2845')
    Quantity = kwargs.get('Quantity', '') #交易張數
    PriceType = kwargs.get('PriceType', '3')
    Price = kwargs.get('PriceType', '0.00')
    CID = kwargs.get('CID', 'Q01')

    data = {
	    "AcctID":AcctID,
	    "CustID":CustID,
	    "ClientIP":ClientIP,
	    "TranDate":TranDate,
	    "BS":BS,
	    "StockID":StockID,
	    "Quantity":Quantity,
	    "PriceType":PriceType,
	    "Price":Price,
	    "CID":CID
	}
    new_order_url = 'http://54.65.120.143:8888/hackathon/eSTKList'
    response = requests.post(new_order_url, json=data)
    response_text = response.text
    response_text=x.replace('\n', '')
	response_text=x.replace(' ', '')
    return response_text

def get_token():

	data = {"CustID":"B299491384","UserID":"B299491384","PIN":"1384","Token":""}
	response = requests.post('http://54.65.120.143:8888/hackathon/login', json=data)
	text = response.text
	token = text[13:-4]

	return token
# @app.route('/visitors', methods=['POST'])
# def put_visitor():
#     user = request.json['name']
#     return 'Hello {}!'.format(user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
