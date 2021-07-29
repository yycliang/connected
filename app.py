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
from similar_text import similar_text


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
collections4 = mongo.db.Following

# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index')
def index():
    if session['username'] == "":
        return render_template('index.html', loggedIn = False)
    else:
        return render_template('index.html', loggedIn = True)
    return render_template('index.html')

@app.route('/dashboard', methods=['GET','POST','ET'])
def dashboard():
    if request.method == "POST":
        id = request.form['objectID']
        posting = collections2.insert(collections.find({"_id":ObjectId(id)}, {"_id": 0}))
        id2 = posting[0]
        collections2.update_one({"_id":id2},{"$set":{"user": session['username'], "status": "interested", "postingID": id}})
    if session['username'] == "":
        return render_template('signup.html', loggedIn = False)
    dashboard = list(collections2.find({"user": session['username']}))
    following = list(collections4.find({"user": session['username']}))
    interested = list(collections2.find({"status":"interested", "user": session['username']}))
    progress = list(collections2.find({"status":"inprogress", "user": session['username']}))
    completed = list(collections2.find({"status":"completed", "user": session['username']}))
    users = list(collections3.find({"email": session['username']}))
    return render_template('dashboard.html', dashboard = dashboard, interested = interested, progress = progress, completed = completed, users = users, following = following, loggedIn = True)
        
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
        if request.form['image_link'] == "":
            image_link = "https://cdn.pixabay.com/photo/2014/05/02/21/50/laptop-336378__480.jpg"
        else:
            image_link = request.form['image_link']
        link = request.form['link']
        date = request.form['date']
        collections.insert({'title': post_title, 'company': post_company, 'description': post_description, 'image': image_link, "link": link, 'date': date})
        return redirect(url_for('postings'))
    if session['username'] == "":
        return render_template('signup.html', loggedIn = False)
    return render_template('postings.html', postings = postings, loggedIn = True)

@app.route('/users')
def users():
    currentUser = session['username']
    inSession = (session['username'] != "")
    users = list(collections3.find({}))
    following = list(collections4.find({"user": session['username']}, {"_id": 0, "fullname": 1}))
    dash = []
    for i in following:
        dash.append(i["fullname"])
    users = [elem for elem in users if elem["fullname"] not in dash]
    if session['username'] == "":
        return render_template('signup.html', loggedIn = False)
    return render_template('users.html', users = users, currentUser = currentUser, inSession = inSession, loggedIn = True)


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
        if session['username'] == "":
            return render_template('login.html', loggedIn = False)
        else:
            return render_template('dashboard.html', loggedIn = True, time=datetime.now())

@app.route('/signup', methods=['POST', 'GET', 'ET'])
def signup():
    if request.method == 'GET':
        if session['username'] == "":
            return render_template('signup.html', loggedIn = False)
        else:
            return render_template('dashboard.html', loggedIn = True, time=datetime.now())
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
                'picture': request.form['picture'], 
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
                'picture':  request.form['newpicture'],
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
    return render_template('progressid.html', job = job, indexes = indexes, loggedIn = True)


@app.route('/search', methods=['GET','POST','ET'])
def search():
    if session['username'] == "":
        return redirect(url_for('login'))    
    postings = list(collections.find({}))
    if request.method == "POST":
        postingSearch = request.form['postingSearch'].title()
        if postingSearch == "":
            return redirect('/postings')
        postings = list(collections.find({}))
        postingMatches = []
        for i in postings:
            if similar_text(postingSearch, i["title"]) > 50:
                postingMatches.append(i)        
        if len(postingMatches) == 0:
            postings = list(collections.find({}))
            return render_template('postings.html', error = "No Results Found. Try Again.", postings = postings, loggedIn = True)
        return render_template('postings.html', postings = postingMatches, loggedIn = True) 
    return render_template('postings.html', postings = postings, loggedIn = True)


@app.route('/follow', methods=['GET','POST','ET'])
def follow():
    if request.method == "POST":
        id = request.form['objectID']
        following = collections4.insert(collections3.find({"_id":ObjectId(id)}, {"_id": 0}))
        id2 = following[0]
        collections4.update_one({"_id":id2},{"$set":{"user": session['username']}})
    return redirect(url_for('dashboard'))


@app.route('/unfollow', methods=['GET','POST','ET'])
def unfollow():
    if request.method == "POST":
        id = request.form['objectID']
        collections4.delete_one({"_id":ObjectId(id)})
    return redirect(url_for('dashboard'))


@app.route('/user/<email>', methods=['GET','POST','ET'])
def user(email):
    if session['username'] == "":
        return redirect("/")
    userPostings = list(collections2.find({"user": email}))
    current = list(collections2.find({"user": session['username']}))
    dash = []
    for i in current:
        dash.append(i["postingID"])
    currentUserPostings = []
    for posting in userPostings:
        if collections2.find({"user": session['username'], "postingID": posting["postingID"]}):
            currentUserPostings.append(list(collections2.find({"user": session['username'], "postingID": posting["postingID"]}))[0])
    userPostings = [elem for elem in userPostings if elem["postingID"] not in dash]
    users = list(collections3.find({"email": email}))
    return render_template('eachUser.html', userPostings = userPostings, currentUserPostings = currentUserPostings, users = users, loggedIn = True)


@app.route('/addFromUser', methods=['GET','POST','ET'])
def addFromUser():
    if request.method == "POST":
        id = request.form['objectID']
        posting = collections2.insert(collections.find({"_id":ObjectId(id)}, {"_id": 0}))
        id2 = posting[0]
        collections2.update_one({"_id":id2},{"$set":{"user": session['username'], "status": "interested", "postingID": id}})
    dashboard = list(collections2.find({"user": session['username']}))
    following = list(collections4.find({"user": session['username']}))
    interested = list(collections2.find({"status":"interested", "user": session['username']}))
    progress = list(collections2.find({"status":"inprogress", "user": session['username']}))
    completed = list(collections2.find({"status":"completed", "user": session['username']}))
    users = list(collections3.find({"email": session['username']}))
    return render_template('dashboard.html', dashboard = dashboard, interested = interested, progress = progress, completed = completed, users = users, following = following)