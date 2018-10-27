from flask import Flask, make_response
import json

app = Flask(__name__)


@app.route('/')
def search():
    response = make_response(json.dumps({'text': '1234'}))
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers['Content-Type'] = 'text/json'
    return response
