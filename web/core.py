from flask import Flask, make_response, request
import json

app = Flask(__name__)


@app.route('/')
def search():
    query = request.args.get('query')
    max_docs = request.args.get('max_docs')
    response = make_response(json.dumps({'text': query}))
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers['Content-Type'] = 'text/json'
    return response
