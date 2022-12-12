import json

from datetime import datetime
from flask import Flask
from flask import request
from flask import jsonify

from deta import Deta


deta = Deta("pass-manager")
db = deta.Base('simpleDB')
app = Flask(__name__)

@app.route('/', methods=["GET"])
def hello_world():
    response = {'message':'Hello World'}
    return jsonify(response)

@app.route('/register', methods=["POST"])
def create_password():
    name = request.json.get("name")
    pwd = request.json.get("pwd")
    now = datetime.now()

    insert = db.put({
        "name":name,
        "password": pwd,
        "updated": now.strftime("%d/%m/%Y %H:%M:%S")
    })

    return jsonify(insert, 201)

@app.route("/load", methods=["GET"])
def get_register(key):
    pwd = db.get(key)
    return pwd if pwd else jsonify({"error":"Not Found"}, 404)