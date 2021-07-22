# Build a Community Board with Flask and MongoDB (with a little help from PyMongo)
## Extensions

1. [Extensions](#extensions)
    1. [Individual Post Pages](#individual-post-pages)
    2. [User Accounts](#user-accounts)
        1. [New User Sign Up](#new-user-sign-up)
        2. [Logging In](#logging-in)
        3. [Logging Out](#logging-out)
        4. [Gated Pages](#gated-pages)
2. [Reach Extensions](#reach-extensions)
    1. [Date Formatting](#date-formatting)
    2. [Environment Variables](#environment-variables)
    3. [Password Hashing](#password-hashing)
    4. [Uploading Files](#uploading-files)

## Extensions

### Individual Post Pages

Now that we have individual posts stored in our MongoDB database with unique identifiers, `_id`'s, we can consider how to show a unique page for each. Adding a new route for each new post would be massively inefficient, so instead, we'll make use of variables in the route name and definition.

Before we write a new route, we'll want to make sure we've installed the `bson` module. The `bson` module will help us convert `ObjectId`s into usable strings we can more-easily work with in our database.

```bash
pip install bson
```
> Remember to add the `--user` flag in [ide.cs50.io](https://ide.cs50.io).

We'll need to add an import statement in our app, as well:

```python
from bson.objectid import ObjectId
```

Next we'll write a new route that includes the `<eventID>` variable as part of the route name itself. We'll then pass that same `eventID` variable to the `event()` function.

In the `event()` function:

- We first define the collection in the MongoDB we plan to use.
- Then we'll filter the collection to retrieve only the event that has an `_id` that matches the `eventID` variable. Since each `_id` is unique, we can use the `.find_one({})` method which will return a single entry from the collection (which doesn't require iteration).
- This event is then passed to the `event.html` template to be rendered for the user.

```python
@app.route('/events/<eventID>')

def event(eventID):
    collection = mongo.db.events
    event = collection.find_one({'_id' : ObjectId(eventID)})

    return render_template('event.html', event = event)
```

And an HTML snippet to show the filtered data:

```html
<div>
    <h1>{{ event.event }} ({{ event.date }})</h1>
    <h3>Posted by {{ event.user }}</h3>
</div>
```

### User Accounts & Sessions

> Resist the temptation to go too deep into "What is a session? What is a cookie?" your first time through.

A common feature of many apps is that they allow the creation of user accounts. To do this, a few things need to happen:

- [New User Sign Up](#new-user-sign-up)
- [Logging In](#logging-in)
- [Logging Out](#logging-out)
- [Gated Pages](#gated-pages)

Before we address each of these actions, it's worth nothing *how* the app will know whether a user is logged in. To keep track of whether a user is logged in, we'll use the `session` variable that is part of any browser. The `session` variable is stored in the browser memory, and we can access it using a function built into Flask: `session`.

To bring in the `session` function from Flask, we'll update the import statement in our app. 

```python
from flask import render_template, request, redirect, session, url_for
```

> Note, we're also adding the `url_for` function which will be used to simplify how a user is passed from one page to another.

To be able to use the `session` functionality, we need to store a secret key that will be used to sign each session. The `secret_key` will be a property of the app itself:

```python
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
```

Now that a session can be created, we can assign a value to a property of the `session` variable in order to store that value:

```python
session['username'] = "My Name"
```

To access that variable, we can call the `session` variable and the property name:

```python
print(session['username'])
# My Name
```

We can also write logic statements to capture whether the `session` variable contains a particular property:

```python
if 'username' in session:
	# some code here
```

> Read more about sessions and secret keys in the [Flask documentation](http://flask.pocoo.org/docs/1.0/quickstart/#sessions).

### New User Sign Up

In order for a new user to sign up, a few things need to happen:

1. We need to show the user the `signup.html` template (via a `GET` request).
2. Once they've filled out the form on that template, we need to check the database to see if we can find that user (via a `POST` request and `.find_one()`.
3. If we can find that user, then they already exist, so a new user cannot sign up with the same name.
4. If we cannot find that user, then that user does not yet exist, so we can create it.
5. To create the new user in the database, we can `.insert()` the `username` and `password` we get from the form.
6. We then start a new session with the `username` from the form.
7. Lastly, we redirect the user to the homepage.

Here's an HTML snippet we could use on `signup.html` to capture a username and password:

```html
<form action="/signup" method="POST">
    <label for="name">Name</label>
    <input type="text" name="username">
    <label for="password">Password</label>
    <input type="password" name="password">
    <input type="submit" value="Sign Up">
</form>
```

And here's a corresponding route that can be used to handle signup data:

```python
@app.route('/signup', methods=['POST', 'GET'])

def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            users.insert({'name' : request.form['username'], 'password' : request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists! Try logging in.'

    return render_template('signup.html')
```

> Since we don't (yet) have a way for a user to log out, you can clear the session cookie using your browser's Developer Tools.

#### Extensions

- Consider where you might want to show the user they are logged in.
- Consider what else a user would expect to see when signing up.
- Also consider what a user should do if they already have an account? (see below)
- Think about why we only store the `username` in the session. Why don't we also store the password? Is this the most secure way to store credentials?

### Logging In

Now that a user has signed up, they'll need a way to sign back in in the future. To account for this, we may want a new `login` route. This route should:

1. Consult the MongoDB and find the user who is trying to log in.
2. If the user is in the database, compare the password submitted by the user to the password stored in the database.
    1. If the passwords are the same, a new session will be started for the user and the user will be routed to the index page.
    2. Otherwise, they will receive a message indicating an invalid username/password combination.

Here's an HTML snippet for a login. Notice how it also includes a link to the `signup` route in case a user doesn't yet have an account.

```html
<h2>Log in</h2>
<div>
    <form action="/login" method="POST">
        <label for="name">Name</label>
        <input type="text" name="username">
        <label for="password">Password</label>
        <input type="password" name="password">
        <input type="submit" value="Log In">
    </form>
    <p>No account? <a href="/signup">Sign up.</a></p>
</div>
```

And here's a corresponding route.

```python
@app.route('/login', methods=['POST'])

def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if request.form['password'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'
```

#### Extensions

- Consider where you might want to include a form to "Log In"
- Consider how you would only show the login form to a user who isn't logged in (e.g. doesn't yet have a session started).

### Logging Out

Once a user is logged in, they may also want to log out. Logging out is as simple as clearing the stored session data and redirecting to another page.

```python
@app.route('/logout')

def logout():
    session.clear()
    return redirect('/')
```

#### Extensions

- Consider where in your HTML templates you may want to include a link to "Log Out".

### Gated Pages

Sometimes you may have pages that you don't want everyone to be able to see, e.g profile/account information or a list of the events/items a user has submitted. Maybe you only want to show information when a user is logged in and it is that same user's information you want to show.

Using what we already know, think about how to write a new route that shows a template populated by data from the database filtered by the name stored in `session['username']`. An example solution is shown below.

We can add a new route:

```python
@app.route('/events/myevents')

def myevents():
    collection = mongo.db.events
    username = session['username']
    events = collection.find({'user' : username})

    return render_template('my_events.html', events = events)
```

And also a new snippet for an HTML template:

```html
<div>
    <ul>
        {% for event in events %}
            <li><a href="/events/{{event._id}}">{{ event.event }} - {{ event.date }}</a>(Posted by {{ event.user }})</li>
        {% endfor %}
    </ul>
</div>
```

#### Extensions

- Consider where in your HTML template(s) you might want to include a link to "My Events"
- Think about how you might only show the "My Events" link to a user who is logged in.

## Reach Extensions

Now that you have a sense of the basics, there are loads of directions you and students may want to take the framework you've built so far. Here we touch on three possible reach extensions:

- [Date Formatting](#date-formatting)
- [Environment Variables](#environment-variables)
- [Password Hashing](#password-hashing)

### Date Formatting

> Resist the temptation to go too deep into "What is a date? What is a time?" your first time through.

Formatting dates in python is done using the `datetime` module. `datetime` is already built into Python 3, but you may want to ensure it's installed using:

```bash
pip install datetime
```
> Remember to add the `--user` flag in [ide.cs50.io](https://ide.cs50.io).

Then import the `datetime` functions into your app:

```python
from datetime import datetime
```

There are two functions you may find useful for reformatting dates: `strptime` and `strftime`.

#### `strptime`

`strptime` is short for "string parse time" and takes a string as an argument and returns a DateTime Object. It does this according to a format that you define by using variables that represent different parts of a date/time: e.g. `%d` is the day of the month as a zero-padded decimal number, and `%Y` is the year with century as a decimal number. The [documentation](https://docs.python.org/3.7/library/datetime.html#strftime-and-strptime-behavior) has the full list of options.

So to convert the string `04-10-19` into a DateTime Object, we need to recognize that it's in the format of `MM-DD-YY` which would be represented as `%m-%d-%y`. Notice how the dashes are used in the representation just like they're used in the string. `strptime` takes the string and the representation as arguments to output a DateTime Object:

```python
date = "04-10-19"
dateObj = datetime.strptime(date, '%m-%d-%y')
```

#### `strftime`

To represent the DateTime Object in a new way, we can use `strftime` which stands for "string format time". It takes a single argument: the new DateTime format:

```python
dateStr = dateObj.strftime('%a, %b %d, %Y')
print(dateStr)
# Wed, Apr 10, 2019
```

> `%a` is the weekday as locale’s abbreviated name (Sun, Mon, etc.); `%b` is the month as locale’s abbreviated name (Jan, Feb, etc.); `%d` is the day of the month as a zero-padded decimal number (01, 02, etc.); and `%Y` is the year with century as a decimal number (2000, 2001, etc.).

#### Extensions

- `datetime` also includes support for parsing and formatting times, timezones, and various localization/languages.
- Try using `datetime` to display 24-hour time (e.g. 18:00) instead of 12-hour time (e.g. 6:00pm).

#### Resources

- [Python 3.7 datetime Documentation](https://docs.python.org/3.7/library/datetime.html)

### Environment Variables

> Resist the temptation to go too deep into "What is an environment variable?" your first time through.

Environment variables are used to protect sensitive usernames and passwords. By hiding credentials, it is much more difficult for anyone to gain unauthorized access to sensitive data.

Credentials are listed in a file called `.env`, and that should always then be listed in a repository's `.gitignore` file. By including `.env` in the `.gitignore`, the `.env` file will not be uploaded and shared to github. Instead, we will be able to use the credentials when we develop in our local environment, and when we push to the cloud we'll need to make sure to securely store the credentials in the platform itself.

To use environment variables, we first need to install the `python-dotenv` module (and the `os` module) using the Terminal:

```bash
pip install os # if you haven't already
pip install python-dotenv
```
> Remember to add the `--user` flag in [ide.cs50.io](https://ide.cs50.io).

And we need to include the `load_dotenv` function in our app:

```python
import os # if you haven't already
from dotenv import load_dotenv
```

Next, we create a new file called `.env` and list the credentials we want to store there:

```
MONGO_USERNAME="admin"
MONGO_PASSWORD="password"
```

Back in our app, the `load_dotenv` function loads the variables from the `.env` file so we can use variable names in place of the credentials themselves.

```python
# first load environment variables in .env
load_dotenv()

# then store environment variables with new names
USER = os.getenv("MONGO_USERNAME")
PASS = os.getenv("MONGO_PASSWORD")
```

Now whenever we want to use the credentials, we can just use the name of the variable instead of the credential itself.

Recall the code we use to connect to our MongoDB:

```python
app.config['MONGO_URI'] = 'mongodb+srv://admin:password@server-kxrbn.mongodb.net/test?retryWrites=true'
```

Using environment variables, it is now secured:

```python
app.config['MONGO_URI'] = 'mongodb+srv://'+USER+':'+PASS+'@server-kxrbn.mongodb.net/test?retryWrites=true'
```

So if someone were to see our code (on github or using other tools), they wouldn't be able to see our username and password.

#### Environment Variables in ide.cs50.io

When you are building in [ide.cs50.io](https://ide.cs50.io), the default file structure does not show hidden/system files.

Create a `.env` file as you would any other file, and save it to the top-level folder; when you save it, you won't actually see it in the list of files. To see the `.env` file, tap the gear in the folder structure and select "Show hidden files".

You'll also see other system files that start with `.` such as `.flaskenv` and `.gitignore`.

> At this point, it's worth checking again that you've listed `.env` in your `.gitignore` file.

#### Environment Variables in Heroku

When you deploy your app to heroku, you do not include the `.env` file. Instead, heroku has it's own secure storage location for listing environment variables.

For your deployed app to function on Heroku, you can either set the environment variables from the Heroku Dashboard or using the Terminal.

##### Heroku Dashboard

After logging into Heroku, you should see the name of your deployed project. Click on that project name:

![Initial View in Heroku Dashboard](screenshots/heroku-dashboard-1.png "Initial View in Heroku Dashboard")

Then from the Dashboard, choose "Settings":

![Settings View in Heroku Dashboard](screenshots/heroku-dashboard-3.png "Settings View in Heroku Dashboard")

There, you'll see "Config Vars", and tapping "Reveal Config Vars" will provide an interface for adding each environment variable.

![Config Vars in Heroku Dashboard](screenshots/heroku-dashboard-5.png "Config Vars in Heroku Dashboard")

Once you finish, you can "Hide Config Vars".

##### Heroku Command Line Interface

You can view current config var values using:

```bash
heroku config
# GITHUB_USERNAME: joesmith
# OTHER_VAR:    production
```

Or view a specific config variable using:

```bash
heroku config:get GITHUB_USERNAME
# joesmith
```

Set a config variable using:

```bash
heroku config:set GITHUB_USERNAME=joesmith
# Adding config vars and restarting myapp... done, v12
# GITHUB_USERNAME: joesmith
```

Remove a config variable using:

```bash
heroku config:unset GITHUB_USERNAME
# Unsetting GITHUB_USERNAME and restarting myapp... done, v13
```

> Review the [Heroku documentation for creating and storing vars](https://devcenter.heroku.com/articles/config-vars).

#### Resources

- [python-dotenv on GitHub](https://github.com/theskumar/python-dotenv)

### Password Hashing

> Resist the temptation to go too deep into "What is a hash? What's the best way to store passwords?" your first time through.

So far, we've asked users to come up with a username and a password, however we're storing that password in plaintext in our database. Storing passwords in plaintext is **highly insecure** because if someone who isn't authorized gains access to the database, they would have access to all users' passwords.

To store passwords more securely, we can hash the password, and store that value instead. Then when a user tries to log into the app, we'll compare the hash of the password they provide to the hash of the password that is stored in the database. If they two match, we grant access; if they don't, then we deny access.

> The benefit of using a hash is that it cannot (practically) be unhashed. Unlike encryption/decryption, the hash is a one-way function, so even if someone gets a hash, they cannot work backwards to figure out the original password input.

To hash passwords, we'll use the `bcrypt` module:

```bash
pip install bcrypt
```
> Remember to add the `--user` flag in [ide.cs50.io](https://ide.cs50.io).

And we need to import `bcrypt` into our app:

```python
import bcrypt
```

We can now modify the `signup` route to generate and store the hash of the password provided by the user:

```python
@app.route('/signup', methods=['POST', 'GET'])

def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : str(hashpass, 'utf-8')})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists! Try logging in.'

    return render_template('signup.html')
```

And we can modify the `login` route to check that the hash of the password provided matches the stored password hash for a given user:

```python
@app.route('/login', methods=['POST'])

def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw((request.form['password']).encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'
```

Sign up with a new user to see how `bcrypt.hashpw()` generates and stores a hashed password instead of the plaintext password.

#### Extensions

- Explore other hashing algorithms, e.g. SHA-256
- Explore how "salts" are used to complicate stored password hashes

#### Resources

- [The bcrypt Project](https://pypi.org/project/bcrypt/)

### Uploading Files

Check out this video for some guidance on uploading files: [youtube.com/watch?v=DsgAuceHha4](https://www.youtube.com/watch?v=DsgAuceHha4)