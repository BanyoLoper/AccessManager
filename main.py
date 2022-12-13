import os

from datetime import datetime
from flask import Flask, request, jsonify

from deta import Deta


deta = Deta(os.getenv('PROJECT_KEY'))
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

    insert = db.insert({
        "name":name,
        "password": pwd,
        "updated": now.strftime("%d/%m/%Y %H:%M:%S")
    })

    return jsonify(insert, 201)
    # return jsonify({"name": name, "pwd": pwd, "updated": now.strftime("%d/%m/%Y %H:%M:%S")})

@app.route("/load", methods=["GET"])
def get_register(key):
    pwd = db.get(key)
    return pwd if pwd else jsonify({"error":"Not Found"}, 404)