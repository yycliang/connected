# ---- YOUR APP STARTS HERE ----
# -- Import section --
import pymongo
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_pymongo import PyMongo
from flask_pymongo import ObjectId
from datetime import datetime
from flask import session, url_for
import os
# from flask_pymongo import PyMongo


# -- Initialization section --
app = Flask(__name__)

app.config['URI'] = os.getenv("URI")
URI = app.config["URI"]

# name of database
app.config['MONGO_DBNAME'] = 'Connected'

# URI of database
app.config['MONGO_URI'] = URI

mongo = PyMongo(app)

# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
@app.route('/postings')
def postings():
    return render_template('postings.html')
@app.route('/profile')
def profile():
    return render_template('profile.html')

