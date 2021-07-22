# Build a Community Board with Flask and MongoDB (with a little help from PyMongo)

1. [Intro](#intro)
    1. [Show Me a Demo First](#show-me-a-demo-first)
    2. [How'd You Make That?](#howd-you-make-that)
2. [Initial Setup](#initial-setup)
    1. [Sign Up for MongoDB](#sign-up-for-mongodb)
        1. [Create a database](#create-a-database)
        2. [Create a database user](#create-a-database-user)
        3. [Whitelist IP addresses](#whitelist-ip-addresses)
    2. [Connect to MongoDB](#connect-to-mongodb)
3. [Push Data to MongoDB](#push-data-to-mongodb)
4. [Queries of MongoDB](#queries-of-mongodb)
    1. [Sorting and Limiting Query Results](#sorting-and-limiting-query-results)
6. [Push to Heroku](#push-to-heroku)

## Intro

Now that you and your students have built an app using Flask, you might have recognized a need to store and retrieve data. You already know how to store data locally, but apps that only store data locally operate in complete isolation. For instance, if two people are using the same app, they can't see what each other adds to their local database.

But what if we want to contribute to something big where people can see each other's posts, likes, or comments? For this, we're going to use a database called MongoDB.

### Show Me a Demo First

Just want to see a demo? [Click here]() [NEED TO ADD LINK TO HEROKU INSTANCE]

> If you're going to show this in a class, be sure to test the link beforehand. It may take Heroku a moment to spin up the server.

If you've come just looking to run the demo code, this is a list of the packages you'll want to make sure you've installed. If you're using your own development environment, these should work as written.

> In [ide.cs50.io](https://ide.cs50.io), you may need to add a `--user` flag at the end of each: `pip install <package> --user`. 

```python
pip install flask
pip install flask-pymongo # for mongodb connection
pip install dnspython # for mongodb connection
pip install bcrypt # for password handling
pip install bson # for page/post
pip install datetime # for prettifying dates
pip install python-dotenv # for .env variables
```

Or all in one:

```python
pip install flask flask-pymongo dnspython bcrypt bson datetime python-dotenv
```

And you'll need to export these variables in the Terminal:

```bash
export FLASK_APP=main.py
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=8080
export FLASK_DEBUG=1
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
```

To view the finished app:

- First create a `.env` file with these credentials:
```bash
MONGO_USERNAME="admin"
MONGO_PASSWORD="6zCs4vJtrzwkLBqL"
```
- Then rename the `routes.py` starter template to anything else, and rename `routes-complete.py` to `routes.py`.
- Lastly, execute `flask run` in the Terminal as before.

> Test out how to submit an event, sign up, log in, view an event page, and log out.
> 
> Examine (the newly named) `routes.py` to see how each action is implemented.

### How'd You Make That?

Read on for the steps and lessons to build that completed Flask + MongoDB app.

## Initial Setup

> Although you may be tempted to dive into a mini-lesson about "What is a database? What makes a good database?" because it's tempting to want to share every bit of background knowledge with students, our experience has taught us that students need to see **that** the app can work before they become interested in the nuances of **why** it works exactly as it does. So don't feel like you ought to spend much time on this concept your first time through.
> 
> We've also picked out a few other times in these lessons where you may be tempted to dive deep into a topic, but it may be better to reserve that enthusiasm.

### Sign Up for MongoDB

To get started using MongoDB as a database, you'll want to sign up for an Atlas (free) account at [mongodb.com](https://www.mongodb.com/). The sign up process is a bit lengthy, but it involves:

- Signing up with a (valid) email address
  > If you're demoing this sign-up for students and you have a gmail account you've already used to sign up, consider using `yourname+mongo@gmail.com` (or some variant) to sign up as a new user.
- Submitting your name and creating a password
- When asked to create your first cluster, you can either follow the prompts, or close the dialog box.
- If you close the dialog, you'll be presented with options for the "Cloud Provider" and "Region".
  > We suggest using AWS as the "Cloud Provider" and the region geographically closest to you.
- Choose the "M0" cluster tier to keep things free.
- No "Backup" is needed.
- And you can give the cluster a name or use the default "Cluster0"
- Finally, tap the green "Create Cluster" button.
  > It will take 7-10 minutes to create the cluster, so it's best to create the MongoDB account before taking a break.

While the cluster is being created in the cloud, you can begin the installation of the modules necessary to use MongoDB with Flask:

- a Python toolkit to connect to MongoDB built especially for Flask (`flask-pymongo`), and
- a DNS toolkit for Python (`dnspython`).

In the Terminal:

```bash
pip install flask-pymongo
pip install dnspython
```
> Remember to add the `--user` flag in [ide.cs50.io](https://ide.cs50.io).

Once the cluster is created on MongoDB, we need to do three things to complete the database setup before we can connect to it from our app:

- [Create a database](#create-a-database)
- [Create a database user](#create-a-database-user)
- [Whitelist IP addresses](#whitelist-ip-addresses)

### Create a database

To create a database in the MongoDB interface, click on the name of the cluster, e.g. `Cluster0` and then on the "Collections" heading (or just on the "Collections" button below the cluster name).

![Initial View in MongoDB Interface](screenshots/mongodb-1-initial.png "Initial View in MongoDB Interface")

> You'll notice a MongoDB "checklist" pop up as you get set up. It's worth calling out the user experience of building a new cluster/database/collection on MongoDB. Do students think it's good? bad? intuitive? confusing?

In the "Collections" tab, you'll be prompted with a big green button to "Create Database" - tap that button.

![Collections View in MongoDB Interface](screenshots/mongodb-3-collections.png "Collections View in MongoDB Interface")

You'll then be prompted to give the database a name (it can be anything, e.g. `test`) and to create the first collection by giving it a name (it can also be anything, e.g. `events`). Later, we'll see that when adding data to a database, if you are sending data to a collection that doesn't (yet) exist, MongoDB will create that collection for you. So there's no need to stress about getting this perfect from the beginning.

![Create Database in MongoDB Interface](screenshots/mongodb-5-create-database.png "Create Database in MongoDB Interface")

> You don't need to check "Capped Collection".

We now have our first database! But before we can connect to it, we need to set up our first database user.

### Create a database user

To create a database user, return to the Clusters overview by clicking on "Clusters" in the left sidebar. Once there, select the "Security" tab.

![Security View in MongoDB Interface](screenshots/mongodb-6-create-database-user.png "Security View in MongoDB Interface")

Notice the green button in the top-right corner that says "+ ADD NEW USER" - go ahead and tap that.

Choose a username, e.g. `admin` and (secure) password, e.g. `Ypzb8UvmWKXJsubU`, and make a note of the password you've selected.

> We suggest tapping "Autogenerate Secure Password" to create a compliant password. Then tap "Show" and copy-and-paste the password somewhere safe.

![Add New User in MongoDB Interface](screenshots/mongodb-7-add-new-user.png "Add New User in MongoDB Interface")

When creating a user, you can set various privileges for that user. For this app, we're just going to keep the default "Read and write to any database" permissions.

Tap "Add User" to complete the creation of your first database user!

### Whitelist IP addresses

> Resist the temptation to go too deep into "What is an IP Address?" your first time through.

Now we need to let MongoDB know the IP addresses from which it is safe to access our database and to which it is safe to send data from the database.

Still on the "Security" tab, you'll now see the user you just created. Tap the "IP Whitelist" sub-tab to view a list of the safe IP addresses.

![Whitelist IP Address in MongoDB Interface](screenshots/mongodb-9-ip-whitelist.png "Whitelist IP Address in MongoDB Interface")

Again, tap the green button in the top-right labeled "+ ADD IP ADDRESS".

We're presented with an option to just add the current IP address, to allow access from anywhere, or to list a particular IP address. Since most students will want their app to be accessed by anyone anywhere (and since they should not be storing particularly sensitive data), it's ok to tap the "Allow Access from Anywhere" button. Add a comment, e.g. "Global access", then tap "Confirm".

![Whitelist IP Address in MongoDB Interface](screenshots/mongodb-10-add-whitelist.png "Whitelist IP Address in MongoDB Interface")

> It may take a moment for the "Allow Access from Anywhere" setting to be implemented.

### Connect to MongoDB

To facilitate connecting to MongoDB, we'll be using the module we installed called [Flask-PyMongo](https://flask-pymongo.readthedocs.io/en/latest/). Flask-PyMongo is a set of Python tools for interacting with MongoDB that have been wrapped to integrate well with Flask.

We've already installed the module, but we needed to import it to our app:

```python
from flask_pymongo import PyMongo
```

To connect to our MongoDB, we need to specify two configuration parameters: 'MONGO_DBNAME' and 'MONGO_URI'. This is done by assigning values to two new `app.config` properties:

```python
# name of database
app.config['MONGO_DBNAME'] = 'database-name' 

# URI of database
app.config['MONGO_URI'] = 'mongo-uri'
```

We should replace `database-name` with the name of the database we created in the MongoDB interface, e.g. `test`.

To get our `mongo-uri`, we need to head back to the MongoDB interface. Click to the "Overview" tab, and tap the "Connect" button below the name of the cluster.

![Overview in MongoDB Interface](screenshots/mongodb-11-overview.png "Overview in MongoDB Interface")

Here we'll choose the middle option, "Connect Your Application".

![Connect to Cluster in MongoDB Interface](screenshots/mongodb-12-connect-to-db.png "Connect to Cluster in MongoDB Interface")

Because we're using Python 3.7, we want to select the "Python" driver and the version of "3.6 or later". That will populate the Connection String Only box with a URI that is (mostly) the `mongo-uri`.

![Connect to Cluster in MongoDB Interface](screenshots/mongodb-13-connect-to-db.png "Connect to Cluster in MongoDB Interface")

If you examine the URI closely, you'll notice that our user's username has been included in the URI, as has the database name we previously created, `/test?`. The password, however, is represented as `<password>`. Before we can connect to our database, we'll need to replace `<password>` with our password that we stored somewhere secure.

Setting the configuration parameters should now look like:

```python
# name of database
app.config['MONGO_DBNAME'] = 'test' 

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:Ypzb8UvmWKXJsubU@cluster0-kxrbn.mongodb.net/test?retryWrites=true'
```

> It's worth noting that the default URI in the "Connect Your Application" dialog box is for node.js (3.0 or later), and it is exactly the same as the driver for Python (3.6 or later). If a student misses switching the driver, it won't actually matter.

> It's also worth noting that the second module we installed, `dnspython`, is necessary to account for the `+srv` in the 'MONGO_URI'.

The final part of setting up the connection between our app and our MongoDB is to create a new variable in `routes.py` called `mongo` that will use PyMongo to connect our app to the database using the aforementioned configuration variables:

```python
mongo = PyMongo(app)
```

That may seem like a lot of work to get things set up, but a bit of setup will make our lives a lot easier down the line when we're reading data from and writing data to MongoDB.

### Push Data to MongoDB

#### Write Data Directly to MongoDB

To find out whether our app is correctly configured to connect to our MongoDB, we can add a new route to our app that will just write data to our database:

```python
@app.route('/add')

def add():
    user = mongo.db.users
    user.insert({'name':'Your Name'})
    return 'Added User!'
```

In the `add()` function, we first indicate which collection we want to write data to. In this case, we've selected the `users` collection. What's that? We don't yet have a `users` collection? MongoDB is smart enough to recognize that if we're writing data to a collection that doesn't yet exist, it will first create that new collection then add the data to it.

We next use the `.insert()` method to add a simple JSON object to the database. Here we're only specifying one property, `'name'`, with the value `'Your Name'`. Try replacing `'Your Name'` with your name or other names.

Lastly, the function will return the text "Added User!" on the page.

With Flask running, once you've added this new route and successfully gotten a page that says "Added User!", head back to your MongoDB interface, navigate to your "Collections" (using the "Collections" button on the "Overview"), and notice that you have a new collection called `users`. Clicking on that collection should show a new entry with the name you submitted!

> If you don't see the collection, try tapping "REFRESH" to update the MongoDB Dashboard.

Examine the new entries in your collection. What data did you choose to add, and what data did MongoDB add for you? (look for `_id`'s)

#### Extensions

- Try making the JSON object that is inserted into the collection more complex by adding additional properties (with additional values).
- Try writing to a different collection that does/doesn't exist yet.

#### Using a Form to Collect Data

Using the backend to write data to a database is not very user-friendly. Instead, we'd ideally use a form to collect the user's data and then store that data to the database. Let's do this by adding a new HTML template and a new route:

```html
<form method="post" action="/events/new">
    <label for="event_name">Event Name:</label>
    <input type="text" name="event_name" value="">
    <label for="event_date">Date:</label>
    <input type="date" name="event_date" value="">
    <label for="name">Name:</label>
    <input type="name" name="user_name" value="">
    <input type="submit" value="Submit">
</form>
```

And the corresponding route:

```python
@app.route('/events/new', methods=['GET', 'POST'])

def new_event():
    if request.method == "GET":
        return render_template('new_event.html')
    else:
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        user_name = request.form['user_name']

        events = mongo.db.events
        events.insert({'event': event_name, 'date': event_date, 'user': user_name})
        return redirect('/')
```

By now you should be familiar with the difference between `GET` and `POST` requests. This route shows the user the `new_event.html` template if the page is accessed via a `GET` request. If, however, the route is accessed via a `POST` request, it will collect the data from the form and store it to the database.

By now you should also be familiar with the `request` function in Flask. Here it is used to store each of the user-submitted values to a variable. Next the MongoDB collection which is the target for the data is specified, `events`, and new data is added to the collection as a JSON object via the `.insert()` method we saw before. Lastly, the user is redirected to the homepage.

### Queries of MongoDB

> Resist the temptation to go too deep into "What is a query?" your first time through.

We've now seen how to write data to MongoDB, but we also want to read (and display) data from MongoDB. To do this, we will need to query, or request particular data from, MongoDB.

PyMongo and Flask-PyMongo have a number of useful built-in query methods:

- `.find({})` - will find multiple entries that match the criteria in the `{}`. Returns all documents that match the criteria.
- `.find_one({})` - will find a single entry that matches the criteria in the `{}`. Returns a single document.
- `.find_one_and_delete({})` - will find and delete one document that matches the criteria in the `{}`.
- `.find_one_and_replace({}, {})` - will find one document that matches the criteria in the first `{}` and replace it with the second `{}`.

> Read about additional query methods in the [PyMongo API Documentation](http://api.mongodb.com/python/current/api/pymongo/collection.html)

To see querying in action, we'll start with the most general search of all. Using the `.find({})` method with empty `{}` (or with no `{}` at all) will return all items in the collection.

Let's write a new route to view all of the entries stored in a collection: 

```python
@app.route('/events')

def events():
    collection = mongo.db.events
    events = collection.find({})

    return render_template('events.html', events = events)
```

Again, we first define the collection in our MongoDB we want to query. We then run the `.find({})` query on that collection and store the results in the `events` variable which is sent to the template in the `render_template()` function.

And an HTML snippet for that route:

```html
<div>
    <ul>
        {% for event in events %}
            <li>{{ event.event }} - {{ event.date }}</li>
        {% endfor %}
    </ul>
</div>
```

> We use the handlebar-percent syntax to execute a `for` loop over all of the entries in the `events` array. This will result in creating all of the `<li>`'s within the `<ul>`, one for each entry in `events`.

But what if instead of all documents, you only wanted to find the ones that match some criteria? The method you should use will depend on whether or not the result of the query is unique.

If the query may return multiple documents, you can use the `.find({})` method with search criteria to match against, e.g.:

```python
events = collection.find({'event' : 'Submit Homework'})
```

This would find *all* events for which the `event` property is `'Submit Homework` and return an iterable object.

But what if you know there's only one such entry, for example when searching a list of users for only one particular user (since users must be unique). Instead of using the `.find({})` query method, we can use the `.find_one({})` query method:

```python
user = users.find_one({'name' : 'My Name'})
```

The `.find_one({})` query method returns just the object itself instead of returning something you would have to iterate (or loop) over. This method is particularly useful when searching a collection in which documents are assigned unique id's.

### Sorting and Limiting Query Results

In addition to finding documents that match a particular query, you may also want to sort the results and/or limit the search to the first n-many results. PyMongo has two methods to help us do just that.

#### Sorting Query Results

The `.sort()` method is used to rearrange the documents that are returned according to some criteria. For example, to sort the events from oldest to newest, we might sort by a `date` parameter and provide an indicator that we want the results in *ascending* order (`1`):

```python
events = collection.find({}).sort('date', 1) 
```

If we wanted the results in descending order from newest to oldest, we just switch the `1` to `-1`:

```python
events = collection.find({}).sort('date', -1) 
```

It is also possible to sort data by multiple fields, e.g.:

```python
events = collection.find({}).sort([('date', pymongo.ASCENDING), ('price', pymongo.DESCENDING)]) 
```

This query would find all events, then sort the results first by date (oldest to newest), then by price (highest to lowest).

#### Extensions

- Consider how a user would find it most useful to see the data represented, then design a corresponding query. 

#### Limiting Query Results

The `.limit()` method is useful for larger datasets where you may only want to show a few results. This query would only show the first 10 documents in a collection:

```python
events = collection.find({}).limit(10) 
```

#### Complex Queries

`.sort()` and `.limit()` can be chained together with `.find({})` to produce complex queries. This query would sort all entries in a collection by the `date` field (newest to oldest) and then include only the first 5:

```python
events = collection.find({}).sort('date', -1).limit(5) 
```

> According to the [documentation](https://docs.mongodb.com/manual/reference/method/db.collection.find/#combine-cursor-methods), `.sort()` is always run before `.limit()` irrespective of the order in which they are chained.
> ```python
> # These produce equivalent results
> events = collection.find({}).sort('date', -1).limit(5)
> events = collection.find({}).limit(5).sort('date', -1)
> ```

> Also check out the [MongoDB Python Documentation for Iterating Over Query Results](http://api.mongodb.com/python/current/api/pymongo/cursor.html)

### Push to Heroku

When your app is working in the cloud environment on [ide.cs50.io](https://ide.cs50.io), you can choose to deploy it to Heroku as you've done before.

> Note: you may want to run `git remote -v` and confirm that **your** username is in the URL. If it isn't, review [this video](https://www.youtube.com/watch?v=Ych-U3_Pb4k&list=PLetu2kRAyoeCvogwvGGq94QgATwfj5viJ&index=11) and follow the steps to remove Upperline's `remote` and add your own.

