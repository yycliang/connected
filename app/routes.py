import os
from app import app
from flask import render_template, request, redirect
from flask_pymongo import PyMongo

# name of database
app.config['MONGO_DBNAME'] = 'database-name' 

# URI of database
app.config['MONGO_URI'] = 'mongo-uri' 

mongo = PyMongo(app)


# INDEX

@app.route('/')
@app.route('/index')

def index():
    return "A Community Events Board"


# CONNECT TO DB, ADD DATA

@app.route('/add')

def add():
    user = mongo.db.users
    user.insert({'name':'Your Name'})
    return 'Added User!'


# ADD NEW EVENT VIA FORM

@app.route('/events/new', methods=['GET', 'POST'])

def new_event():
    if request.method == "GET":
        return render_template('new_event.html')
    else:
        user_name = request.form['user_name']
        event_name = request.form['event_name']
        event_date = request.form['event_date']

        events = mongo.db.events
        events.insert({'event': event_name, 'date': event_date, 'user': user_name})
        return redirect('/')


# SHOW ALL EVENTS IN DATABASE

@app.route('/events')

def events():
    collection = mongo.db.events
    events = collection.find({})

    return render_template('events.html', events = events)


