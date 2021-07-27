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


# -- Initialization section --
app = Flask(__name__)

# name of database
app.config['MONGO_DBNAME'] = 'Connected'

# URI of database
app.config['MONGO_URI'] = os.getenv("URI")

app.secret_key = os.getenv('SECRET_KEY')

mongo = PyMongo(app)

# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/dashboard', methods=['GET','POST','ET'])
def dashboard():
    collections = mongo.db.Postings
    collections2 = mongo.db.Dashboard
    if request.method == "POST":
        id = request.form['objectID']
        posting = collections2.insert(collections.find({"_id":ObjectId(id)}, {"_id": 0}))
        id2 = posting[0]
        collections2.update_one({"_id":id2},{"$set":{"user": session['username'], "status": "saved"}})
    dashboard = collections2.find({"user": session['username']})
    saved = list(dashboard.find({"status":"saved"}))
    progress = list(dashboard.find({"status":"inprogress"}))
    completed = list(dashboard.find({"status":"completed"}))
    return render_template('dashboard.html', dashboard = dashboard, saved = saved, progress = progress, completed = completed)


@app.route('/postings', methods=['GET','POST','ET'])
def postings():
    collections = mongo.db.Postings
    postings = list(collections.find({}))
    if request.method == "POST":
        post_title = request.form['post_title']
        post_description = request.form['post_description']
        image_link = request.form['image_link']
        collections.insert({'title': post_title, 'description': post_description, 'image': image_link})
    return render_template('postings.html', postings = postings)


@app.route('/users')
def users():
    return render_template('users.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        users = mongo.db.Users
        collections2 = mongo.db.Dashboard
        login_user = users.find_one({'name': request.form['username']})
        if login_user is None:
            return render_template('login.html', error = 'User does not exist. Sign up to create an account.', time=datetime.now())
        if login_user:
            if request.form['password'] == login_user['password']:
                session['username'] = request.form['username']
                dashboard = collections2.find({"user": session['username']})
                saved = list(dashboard.find({"status":"saved"}))
                progress = list(dashboard.find({"status":"inprogress"}))
                completed = list(dashboard.find({"status":"completed"}))
                return render_template('dashboard.html', dashboard = dashboard, saved = saved, progress = progress, completed = completed)
        return render_template('login.html', error = 'Invalid username/password combination. Try again', time=datetime.now())
    elif request.method == 'GET':
        return render_template('login.html', time=datetime.now())


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html', time=datetime.now())
    elif request.method == 'POST':
        users = mongo.db.Users
        existing_user = users.find_one({'name' : request.form['username']})
        if existing_user is None:
            users.insert({
                'name': request.form['username'], 
                'password': request.form['password'],
            })
            session['username'] = request.form['username']
            return redirect('/postings')
        return render_template('signup.html', time=datetime.now(), error = 'User already exists! Try logging in instead.')

@app.route('/change', methods=['GET','POST','ET'])
def change():
    collections2 = mongo.db.Dashboard
    if request.method == "POST":
        id = request.form['objectID']
        status = request.form['status']
        collections2.update_one(
            {"_id":ObjectId(id)},
            {"$set":{"status": status}}
            )
    dashboard = collections2.find({"user": session['username']})
    saved = list(dashboard.find({"status":"saved"}))
    progress = list(dashboard.find({"status":"inprogress"}))
    completed = list(dashboard.find({"status":"completed"}))
    return render_template('dashboard.html', dashboard = dashboard, saved = saved, progress = progress, completed = completed)
