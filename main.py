from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)

port = int(os.getenv('PORT', 8000))

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
    return render_template('profile.html')



# @app.route('/visitors', methods=['POST'])
# def put_visitor():
#     user = request.json['name']
#     return 'Hello {}!'.format(user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
