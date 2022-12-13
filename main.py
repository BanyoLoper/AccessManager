import os

from datetime import datetime
from flask import Flask, request
from flask import jsonify, redirect, url_for, render_template

from deta import Deta


deta = Deta(os.getenv('PROJECT_KEY'))
db = deta.Base('simpleDB')
app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if (request.method == 'POST'):
        if (request.form['username'] != os.getenv('ADMIN_USR') or request.form['password'] != os.getenv('ADMIN_PASS')):
            error = 'Invalid credentials, please try again'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)  


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


@app.route("/load/<key>", methods=["GET"])
def load_key(key):
    pwd = db.get(key)
    return pwd if pwd else jsonify({"error":"Not Found"}, 404)