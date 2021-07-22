import os
from app import app
from flask import render_template, request, redirect
import pyrebase


config = {
  "apiKey": os.environ['FIREBASE_API_KEY'],
  "authDomain": "community-event-manager.firebaseapp.com",
  "databaseURL": "https://community-event-manager.firebaseio.com",
  "projectId": "community-event-manager",
  "storageBucket": "community-event-manager.appspot.com",
  "serviceAccount": "app/firebase-private-key.json",
  "messagingSenderId": "1052538486567"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

@app.route('/')
@app.route('/index')

def index():
    db_events = db.child("events").get().val().values()
    return render_template('index.html', events = db_events)

# NEW EVENT

@app.route('/events/new', methods=['GET', 'POST'])

def new_event():
    if request.method == "GET":
        return render_template('new_event.html')
    else:
        new_event = dict(request.form)
        db.child("events").push(new_event)
        events.append(new_event)
        return redirect('/')
