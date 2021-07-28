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

collections = mongo.db.Postings
collections2 = mongo.db.Dashboard
collections3 = mongo.db.Users

# loggedIn = False
# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index')
def index():
    session['username'] = ""
    return render_template('index.html')


@app.route('/dashboard', methods=['GET','POST','ET'])
def dashboard():
    if session['username'] == "":
        redirect(url_for('login'))
    if request.method == "POST":
        id = request.form['objectID']
        posting = collections2.insert(collections.find({"_id":ObjectId(id)}, {"_id": 0}))
        id2 = posting[0]
        collections2.update_one({"_id":id2},{"$set":{"user": session['username'], "status": "interested", "postingID": id}})
    dashboard = list(collections2.find({"user": session['username']}))
    interested = list(collections2.find({"status":"interested", "user": session['username']}))
    progress = list(collections2.find({"status":"inprogress", "user": session['username']}))
    completed = list(collections2.find({"status":"completed", "user": session['username']}))
    users = list(collections3.find({"email": session['username']}))
    return render_template('dashboard.html', dashboard = dashboard, interested = interested, progress = progress, completed = completed, users = users)
        

@app.route('/postings', methods=['GET','POST','ET'])
def postings():
    postings = list(collections.find({}))
    dashboard = list(collections2.find({"user": session['username']}, {"_id": 0, "postingID": 1}))
    dash = []
    for i in dashboard:
        dash.append(i["postingID"])
    postings = [elem for elem in postings if str(elem["_id"]) not in dash]
    if request.method == "POST":
        post_title = request.form['post_title']
        post_company = request.form['post_company']
        post_description = request.form['post_description']
        image_link = request.form['image_link']
        date = request.form['date']
        collections.insert({'title': post_title, 'company': post_company, 'description': post_description, 'image': image_link, 'date': date})
        return redirect(url_for('postings'))
    return render_template('postings.html', postings = postings)


@app.route('/users', methods=['GET','POST', 'ET'])
def users():
    usersCol = mongo.db.Users
    users = list(usersCol.find({}))
    return render_template('users.html', users = users)

@app.route('/login', methods=['POST', 'GET', 'ET'])
def login():
    if request.method == 'POST':
        login_user = collections3.find_one({'email': request.form['username']})
        if login_user is None:
            return render_template('login.html', error = 'User does not exist. Sign up to create an account.', time=datetime.now())
        if login_user:
            if request.form['password'] == login_user['password']:
                session['username'] = request.form['username']
                return redirect(url_for('dashboard'))
        return render_template('login.html', error = 'Invalid username/password combination. Try again', time=datetime.now())
    elif request.method == 'GET':
        return render_template('login.html', time=datetime.now())

@app.route('/signup', methods=['POST', 'GET', 'ET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html', time=datetime.now())
    elif request.method == 'POST':
        users = mongo.db.Users
        existing_user = users.find_one({'email' : request.form['username']})
        if existing_user is None:
            users.insert({
                'fullname': request.form['fullname'], 
                'email': request.form['username'], 
                'location': request.form['location'],             
                'major': request.form['major'], 
                'github': request.form['github'], 
                'password': request.form['password'],
            })
            session['username'] = request.form['username']
            return redirect('/users')
        return render_template('signup.html', time=datetime.now(), error = 'User already exists! Try logging in instead.')

@app.route('/logout')
def logout():
    session.clear()
    session['username'] = ""
    return redirect('/')

@app.route('/change', methods=['GET','POST','ET'])
def change():
    collections2 = mongo.db.Dashboard
    if request.method == "POST":
        id = request.form['objectID']
        status = request.form['status']
        collections2.update_one(
            {"_id":ObjectId(id)},
            {"$set":
                {"status": status}
            }
            )
        if status == "inprogress":
            collections2.update_one(
            {"_id":ObjectId(id)},
            {"$set":
                {"checklist": []}
                }
            )
    return redirect(url_for('dashboard'))

@app.route('/updateUser', methods=['GET', 'POST', 'ET'])
def updateUser():
    users = mongo.db.Users 
    if request.method == "POST":
        users.update_one(
            {"email": session['username']},
            {"$set":
                {
                'fullname': request.form['newfullname'], 
                'location': request.form['newlocation'],
                'major':  request.form['newmajor'], 
                'github':  request.form['newgithub'],
                }
            }
        )
    return redirect(url_for('dashboard'))

@app.route('/progress/<_id>', methods=['GET','POST','ET'])
def progressid(_id):
    indexes = []
    checklist = list(collections2.find({"_id":  ObjectId(_id)}, {"_id": 0, "checklist": 1}))[0]["checklist"]
    if request.method == "POST":
        checklist = request.form.getlist('jobcheckbox')
    collections2.update_one(
            {"_id":ObjectId(_id)},
            {"$set":{"checklist": checklist}}
            )
    check = list(collections2.find({"_id":  ObjectId(_id)}, {"_id": 0, "checklist": 1}))[0]["checklist"]
    indexes.extend([
        check.count("requirements"),
        check.count("resume"), 
        check.count("coverLetter"),
        check.count("doubleCheck"), 
        check.count("apply"), 
        check.count("call"),
        check.count("interview"), 
        check.count("followUp")
        ])
    job = list(collections2.find({"_id":  ObjectId(_id), "user": session['username']}))
    return render_template('progressid.html', job = job, indexes = indexes)
