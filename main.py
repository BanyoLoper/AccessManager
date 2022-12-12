import json

from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route('/', methods=["GET"])
def hello_world():
    response = {'message':'Hello World'}
    return jsonify(response)
