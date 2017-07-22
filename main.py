from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)

port = int(os.getenv('PORT', 8000))

@app.route('/')
def home():
    return render_template('index.html')
# @app.route('/')
# def home():
#     return render_template('index.html')
# @app.route('/')
# def home():
#     return render_template('index.html')



@app.route('/visitors', methods=['POST'])
def put_visitor():
    user = request.json['name']
    return 'Hello {}!'.format(user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
