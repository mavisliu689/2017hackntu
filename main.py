from flask import Flask, render_template, \
	request, jsonify, render_template_string, Response,\
	stream_with_context


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

@app.route('/list_r', methods=['POST'])
# @app.route('/list_r')
def list_r():
    # print (request.)
    # data = request.get_data()
    # json_data=json.loads(data)
    # print (json_data)
   
    try:
        data = request.get_data()
        json_data=json.loads(data)
        print (data)
        invest_score = json_data.get('invest_score')
        industry_type = json_data.get('industry_type')
        topics = json_data.get('topics')
        risks = json_data.get('risk')
    except Exception as e:
        print (e)
        invest_score = "PR1" #RR1,RR2,RR3

        industry_type = ["金融業", "食品工業", "化學工業"]
        topics = ["經濟績效", "間接經濟衝擊", "市場形象/企業品牌"]
        risks = ["商譽／企業形象", "市場風險"]
    print (invest_score, industry_type, topics) 
    stock_ID = [2845,6005,1704,1727,2409,1216,1722,2856,1535]    
    data_frame_topics, data_frame_risks, data_frame_ranking = get_all_excel()
    get_stock_select_industry_type = base_on_stock_ID_get_dataframe(data_frame_topics, stock_ID)
    get_topics_frame = get_topics(get_stock_select_industry_type, topics)
    get_risk_frame = get_risk(data_frame_risks, get_topics_frame, risks)
    get_risk_frame = isnan_tozero(get_risk_frame)
    get_ranking_frame = get_ranking(data_frame_ranking, get_risk_frame)
    get_ranking_frame = isnan_tozero(get_ranking_frame)
    result_industrys = list()
    for index, row in get_ranking_frame.iterrows():
        result_industry = {}
        result_industry.update({
            "name":row['企業完整名稱'],
            "industry_type":row['產業類別'],
            "stock_id": row['股票代碼'],
            "PR": row['社會PR'],
            "stock_type": row['股票類型']
        })
        result_industrys.append(result_industry)
    print (result_industrys)

#     # return render_template('list.html')
#     return render_template('list.html', data=result_industrys)

    return render_template('list.html', data=json.dumps(result_industrys), mimetype='application/json')
    #Response(stream_template('list.html', data=result_industrys))
    # return Response(stream_with_context(json.dumps(result_industrys)))

# def stream_template(template_name, **context):
#     app.update_template_context(context)
#     t = app.jinja_env.get_template(template_name)
#     rv = t.stream(context)
#     rv.enable_buffering(5)
#     return rv

@app.route('/csr_info')
def csr_info():
	return render_template('csr_info.html')

@app.route('/list_all')
def list_all():
    data_frame_topics, data_frame_risks, data_frame_ranking = get_all_excel()
    get_ranking_frame = isnan_tozero(data_frame_ranking)
    result_industrys = list()
    for index, row in get_ranking_frame.iterrows():
        result_industry = {}
        result_industry.update({
            "name":row['企業完整名稱'],
            "industry_type":row['產業類別'],
            "stock_id": row['股票代碼'],
            "PR": row['社會PR'],
            "stock_type": row['股票類型']
        })
        result_industrys.append(result_industry)
    return render_template('list.html', data=json.dumps(result_industrys), mimetype='application/json')

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
    stock_info=stock_info.replace('\n', '')
    stock_info=stock_info.replace(' ', '')
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
    response_text=response_text.replace('\n', '')
    response_text=response_text.replace(' ', '')
    return response_text

def get_token():

	data = {"CustID":"B299491384","UserID":"B299491384","PIN":"1384","Token":""}
	response = requests.post('http://54.65.120.143:8888/hackathon/login', json=data)
	text = response.text
	token = text[13:-4]

	return token


import pandas as pd
import xlrd	
# @app.route('/visitors', methods=['POST'])
# def put_visitor():
#     user = request.json['name']
#     return 'Hello {}!'.format(user)
def get_all_excel():
#     data_frame = pd.read_excel('./2017hackntu/2016_CSR_Data_458_B_index.xlsx',error_bad_lines=False)
    data_frame_topics = pd.read_excel('./data/2016_CSR_Data_458_D_topics_new.xlsx')
    data_frame_risks = pd.read_excel('./data/2016_CSR_Data_458_B_risks.xlsx')
    data_frame_ranking = pd.read_excel('./data/2016_CSR_Data_458_Ranking.xlsx')
    return data_frame_topics, data_frame_risks, data_frame_ranking

def base_on_stock_ID_get_dataframe(data_frame_topics, stock_ID):
    return data_frame_topics[data_frame_topics['股票代碼'].isin(stock_ID)]

def get_industry(stock_select_industry, industry_type):
    print (get_stock_select_industry_type)
    return stock_select_industry[stock_select_industry['產業類別'].isin(industry_type)]

def get_topics(industry_frame, topics):
    industry_frame_c = industry_frame.copy(deep=True)
    industry_frame_c['分數'] = 0
    for topic in topics:
        industry_frame_c.loc[industry_frame_c[industry_frame_c[topic].isin(['1'])].index, ['分數']] += 1
    return industry_frame_c.sort_values (['分數'], ascending=[False])

def get_risk(data_frame_risks, get_topics_frame, risks):
    data_frame_risks_c = data_frame_risks.copy(deep=True)
    data_frame_risks_c['分數'] = 0
    is_in_get_topics_dataframe = get_topics_frame['產業類別']
    data_frame_risks_c = data_frame_risks_c[data_frame_risks_c['產業類別'].isin(is_in_get_topics_dataframe)]
    for risk in risks:
        data_frame_risks_c.loc[data_frame_risks_c[data_frame_risks_c[risk].isin(['1'])].index, ['分數']] += 1
    return data_frame_risks_c.sort_values (['分數'], ascending=[False])

def get_ranking(data_frame_ranking, get_risk_frame):
    is_in_get_risks_dataframe = get_risk_frame['股票代碼']
    return data_frame_ranking[data_frame_ranking['股票代碼'].isin(is_in_get_risks_dataframe)]

def isnan_tozero(get_frame):
    return get_frame.fillna('未上市') 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
