---
title: "Flask Extensions"
course: "PY1"
lesson: "7.1.2"
day: "7"
date: '1/01/2019'
category: 'python'
tags:
  - Flask
  - MVC
  - HTTP methods
  - back-end
---

# Flask Extensions

## Sequence

1. [Exploring the Template](#exploring-the-template)
1. [Static Resources](#static-resources)
2. [Logic in Templates](#logic-in-templates)
3. [Block Content](#block-content)
4. [URL for](#url-for)
5. [Flask Forms](#flask-forms)
6. [Redirects](#redirects)

## Exploring the Template

If you look at it, the file structure is pretty lean. Here's a quick walkthrough of what's there, but emphasize with students that we're just doing this so they have a sense of how the app runs - this isn't something we expect them to memorize.

Settings are stored in the `.flaskenv` and  `.env` files. We won't touch them much, but you'll notice that the first one includes the line `FLASK_RUN_APP=main.py`, which is how our app knows the starting place for this whole app needs to be main.py.

In main.py, we'll see the line of code `from app import app`. If we're tracing this code, ask students where we should look for the next bits of our code. They'll suggest the app directory, and inside that there are only two python files. Most students will correctly assume that `__init__.py` is the first one to run.

In the `__init__.py` file, students will see this:
```python
from flask import Flask

app = Flask(__name__)

from app import routes
```
The first line simply says that we'll be using the Flask framework, so we need to load up that package and call it 'flask'.  The second line creates a new flask app, and the third line tells us which file to execute next.

in the `routes.py` file, that's where it starts getting interesting:
```python
from app import app

@app.route('/')
@app.route('/index')
def index():
  return "Hello world!"
```

We'll spend most of our time today in `routes.py` file, which is where you found the answer to the mini-challenge from a few minutes ago.

## Static Resources
If we want to add **images** and **stylesheets**, we'll need to understand another part of the app called the 'static' directory.

You'll notice that the ONLY way to access templates is by explicitly coding routes out for those pages in our `routes.py` folder, but what about for something like an image, where you need a source, but simply coding in the route doesn't work.

Enter the static folder, a special directory where all the contents CAN be accessed directly. You can actually test it out with students by having them access the image directly. Adding `static/images/micropig.jpeg` to the URL will render the photo even though you never coded out a route for it.

This becomes an exceptionally important tool for things like stylesheets, so the code to load in an image is pretty simple:
```html
<img src="static/micropig.jpg" />
```

Likewise, for stylesheets, you can just access them directly as long as your paths start with 'static':
```html
<link rel="stylesheet" type="text/css" href="static/index.css">
```

> Note: This isn't included in the MVC intro not because it's non-essential, but because it adds a layer of complexity to the introduction that isn't always helpful. it's a pretty easy concept, so work it in where it makes sense.

## Logic in Templates

Templates don't just have to display variable information.
* {{ contents inside double moustache brackets will display on screen }}
* {% contents inside moustache-percent signs like these will run, most often for control flow. %}

Here's an example of how those two types of code might actually work together in a Jinja3 template:
```html
<head>
  {% if pagetitle %}
  <title>{{ pagetitle }} - Shout Your Breakfast</title>
  {% else %}
  <title>Welcome to the Breakfast Shouter!</title>
  {% endif %}
  <link rel="stylesheet" type="text/css" href="static/index.css">
</head>
```

In other words, if there is a `pagetitle` variable passed in through the render_template() function, display it as part of the title, and if there isn't one, then display a more generic title.

> I actually recommend avoiding this type of code for a few reasons. The `endif` is a new idea that is really familiar in languages like Ruby, but since Python usually relies on whitespace (but can't in Jinja3 templates), this concept is more strange to beginners than it is to experienced CS students.
>
> A better way of doing this (that has the added benefit of keeping your templates cleaner), consider adding another method to your model called `generate_title()` that can do this logical piece on the back end. Then you can reliably keep your template written mostly in HTML with occasional python contents added through templating.

## Block Content

One of the coolest features in Jinja templating is the ability to use [block content](http://flask.pocoo.org/docs/1.0/patterns/templateinheritance/) to connect multiple html templates together. That way if you wanted every page to have the same header and navbar, but create the main content separately, doing so is pretty easy.

In this example, we're using base.html to create a navigational bar, and index.html to create our landing page.

`base.html`:
```html
<html>
    <head>
      <title>{% block title %} Shout Your Breakfast {% endblock %}</title>
      <link rel="stylesheet" type="text/css" href="static/index.css">
    </head>
    <body>
        <div>Navigation: <a href="/index">Home</a></div>
        <hr>
        {% block content %}{% endblock %}
    </body>
</html>
```
> the goal here is to have the HTML shell, including a link to a general stylesheet and a link on every page.

`index.html`:
```html
{% extends "base.html" %}

{% block title %}Home - Shout your Breakfast{% endblock %}
{% block content %}
  <h1>Hello, {{ user.username }}!</h1>
  <a href="/posts">Click here to view the blog</a>
  <hr>
  <form method="post" action="/sendBreakfast">
    <label for="nickname">What's your nickname?</label>
    <input type='text' name='nickname'>
    <label for="breakfast">What did you have for breakfast?</label>
    <input type='text' name='breakfast'>
    <input type='submit'>
  </form>
  <img src="static/images/micropig.jpeg" />
{% endblock %}
```
* `extends` tells the template which template to inject these codeblocks into.
* `block ___` and `endblock` let you wrap chunks of code to be injected into the template which is being extended. They'll be injected into the parts of the extended template that matches the names of these blocks.
* This also means any other page can be built on this base template as well, as long as it starts with the `extends "base.html"` and the blocks are correctly named.

## URL For
Instead of hardcoding the addresses of static resources, it's generally condsidered better practice to use the flask method `url_for` in order to generate those addresses dynamically. Aside from this being best practice, it won't likely affect how your student's final projects run in the context of this course, so we don't recommend it to students for this first app.

It's not that complicated though. it really just means that instead of this:
```html
<img src="static/images/micropig.jpeg" />
```

You'll instead use this:
```HTML
<img src="{{ url_for('static', filename='images/micropig.jpeg') }}" />
```

## Flask Forms

While we've handled our form data using Flask requests, that's honestly not best practice, so for students who are ready to dig a little deeper, or who need some features like confirming that an email is valid before submitting, all that can be accomplished with a Flask component called 'Flask-WTF'.

There's a detailed tutorial [here](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms) by Miguel Grinberg, and below are excerpted some snippets from his code to help you see why this might be useful (but also alienating and challenging for first-time learners).

In the HTML template for the form, you generate almost the entire form from python code rather than from HTML:
```html
<form action="" method="post" novalidate>
    {{ form.hidden_tag() }}
    <p>
        {{ form.username.label }}<br>
        {{ form.username(size=32) }}
    </p>
    <p>
        {{ form.password.label }}<br>
        {{ form.password(size=32) }}
    </p>
    <p>{{ form.remember_me() }} {{ form.remember_me.label }}</p>
    <p>{{ form.submit() }}</p>
</form>
```

In the router, you don't hardcode the form data into a dictionary, but rather you use a lot of built-in magic to handle the user's data lot more elegantly.
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)
```

> We're withholding this magic from students up front because the best way to build a production-level app isn't always the best way to learn something new. There's a reason that so many tutorials are called "learn _______ the hard way", mainly because doing something the hard way a few times helps you truly understand and appreciate the beauty of using someone else's library to make it easier.

## Redirects

The router can also be viewed a bit like a control flow document in and of itself. So far we've returned strings, and we've returned rendered templates using the render_template() function. There are several options, but one that students may ask for early on are redirects. Adding those in takes two steps.

1. You have to add 'redirect' to the list of definitions you're importing from Flask. Doing so is pretty simple, just add a comma to your existing list:
```python
from flask import request, redirect
```

Then simply return a redirect when you need to, like in this example, where we redirect anyone who tries to `GET` the `/sendBreakfast` route instead of using a `POST` method as designed.

Be sure to actually code out the route you're redirecting to. Redirecting to `/index` is generally a pretty good trick to teach first-time CS students.
```python
@app.route('/sendBreakfast', methods=['GET', 'POST'])
def handleBreakfast():
    if request.method == 'GET':
        return redirect('/notFound')
    else:
        ... #code to handle `POST` request

@app.route('/notFound')
def handle404():
    return render_template('404.html')
    # Note that this assumes you've created a 404.html template
```
