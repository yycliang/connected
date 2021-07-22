# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
# from flask_pymongo import PyMongo


# -- Initialization section --
app = Flask(__name__)

events = [
        {"event":"First Day of Classes", "date":"2019-08-21"},
        {"event":"Winter Break", "date":"2019-12-20"},
        {"event":"Finals Begin", "date":"2019-12-01"}
    ]

# name of database
# app.config['MONGO_DBNAME'] = 'database-name'

# URI of database
# app.config['MONGO_URI'] = 'mongo-uri'

# mongo = PyMongo(app)

# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html', events = events)


# CONNECT TO DB, ADD DATA

@app.route('/add')

def add():
    # connect to the database

    # insert new data

    # return a message to the user
    return ""
