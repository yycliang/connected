---
title: "Flask Step-by-Step"
course: "PY1"
lesson: "7.1.1"
day: "7"
date: '1/01/2019'
category: 'python'
tags:
  - Flask
  - MVC
  - HTTP methods
  - back-end
---

# Flask Step-by-Step

## Sequence

1. [MVC Framework (includes setup instructions)](#mvc-framework)
2. [Templates](#templates)
3. [HTTP GET Method](#http-get-method)
4. [Routes](#routes)
5. [Templates](#templates)
6. [Forms](#forms)
7. [HTTP POST Method](#http-post-method)
8. [Models](#models)

## MVC Framework

The Model-View-Controller Framework is the general term for the type of app we'll be building. In particular, we're building a Flask app, which is a pretty lean framework - a lot of what happens only works if you explicitly code instructions for it to happen.

#### The restaurant metaphor

We typically use the analogy of a restaurant to help students understand the principles of the MVC framework. We often have students stand up and act this out, in part to have some movement amid a pretty intense lecture, but also as a visual point of reference for later.

To launch this activity, ask students "If you had only ONE person running an entire restaurant, what could go wrong?"
* "That one person would obviously be super busy."
* "If one person calls in sick, the whole restaurant is down."
* "If one person quits, you'd need to find a replacement who can cook, wait tables, take reservations - replacing one person requires finding someone almost impossibly qualified."
Debrief by saying, "That's exactly why we divide complicated programs into smaller pieces. We separate concerns so that if one piece breaks down, the entire program doesn't break, and so that if one method or page needs to be changed, the rest of the site doesn't need to cease operations in order for that to happen."
**The User is like a diner** - A diner reads a menu, makes choices, and then waits for their food. A user interacts with a website, making choices like what to enter into the search bar, and then waits for the results.
**The Model is like a chef** - A chef waits for the customer's order to come in from the waiter, prepares the food, and then sends it back with the waiter. A model is the part of the app that does the *work*. It waits for the user's preferences, finds the results that the user wants to see, and then sends them back to the user.
**The View is like a menu or dinner plate** - This is what the diner SEES. Whether it's the menu up front or the plate with your order on it at the end, the food is what the user imagines when they think of that particular restaurant. In the same way, the view is what the user imagines when they use a particular website - what the customer calls 'pages' are called 'views' in this framework. We'll use templates to create our views.
**The Controller is like the waiter** - The waiter takes your order to the chef, waits for him to prepare your meals, and then brings that meal back to you. The controller takes your input from the first view, hands it to the controller, waits for the results, and then renders the next view for you.

Ask students:
* Why do you think splitting a web application into models, views, and controllers helps? (Answers will vary wildly - validate them all for now and come back to this later)
* Which languages do you think are best suited to each part of the program?
    * Model: Python (or other back-end languages)
    * View: HTML/CSS/JS
    * Controller: This is technically Python as well, but it includes a lot of language borrowed from HTTP (Hypertext Transfer Protocol), so if it looks/feels like a new language, tell students not to panic. That's normal.


#### The template

Here's the [Upperline Flask Template](https://github.com/upperlinecode/flaskproject). Instead of having students FORK this repository, have them clone it down and delete the .git directory. This means they'll have a copy of our example code to reference later.

Code to clone and break reference:
```bash
git clone https://github.com/upperlinecode/flaskproject
cd flaskproject
rm -rf .git
```

#### Running the template

##### Virtual Environments (optional)

If you're running this locally, you may want to run this program inside a virtual environment - that way changes to your Python configuration don't persist and impact other python programs on your machine.

To create a virtual environment (you only need to do this once), run this code in terminal:
```bash
python -m venv venv
```

To ENTER your virtual environment (you'll need to do this every time you open up a new terminal), run this code:
```bash
. venv/bin/activate
```

To EXIT your virtual environment (you'll want to do this if you decide to change projects - think of it like shutting this one down), you just need one word:
```bash
deactivate
```

If you're using a virtual environment like Codenvy, the virtual environment produces more problems than it solves, so consider skipping this step.

##### Python packages

The only packages you need to run are `flask` (for obvious reasons), and `python-dotenv` which allows us to store configuration information in the files `.env` and `.flaskenv`.

To install these packages, run this code.
```bash
pip install flask
pip install python-dotenv
```
Remember, if you're using a virtual environment, these packages will only be installed IN the virtual environment (which is part of why we don't recommend it if you don't need it - students will accidentally forget where they've configured different settings).

If this has worked, and python-dotenv is working, then running a flask application is pretty simple:
```bash
flask run
```

##### Troubleshooting package installation

If your IDE throws errors on either of these commands saying that you aren't authorized, your account may not be authorized to install packages on the IDE you're using, so try adding the 'switch user and do' command ('sudo' for short):
```bash
sudo pip install flask
sudo pip install python-dotenv
```

If you encountered errors with the python-dotenv package, we can still configure those settings manually. You'll need to run these commands once each time you open a terminal:
```bash
export FLASK_APP=main.py
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=8080
export FLASK_DEBUG=1
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
```

After that you should be able to execute the `flask run` command normally.

#### First Test

Navigate to the provided IP address, which is likely something like http://0.0.0.0:8080/ -- Students will be quick to point out that it doesn't work, which is actually to be expected. `0.0.0.0` is a special IP address that means "this machine", but the computer your on (a macbook, a chromebook, a PC, whatever) and the IDE are different machines, we need a replacement IP address that will help us access the contents of the virtual machine (the IDE) instead of our own computers.

We need to a use a feature in the IDE called port forwarding, which will forward the content we're currently serving to 0.0.0.0:8080 to an IP address and port that are accessible from anywhere.

When you arrive, you'll see a very underwhelming "hello world!". **Challenge students to find where this page is.** Where is this 'hello world' coming from?

THEN ask them what the last part of the web address is. This is especially hard in Chrome, because that browser hides the final `/` character in the URL. But depending on what browser they're using, after the port 8080, they're seeing either a `/` or a `/index`.

The best way to make this apparent is to take a quick diversion to a site with really good RESTful routing. If YOU are fuzzy with HTTP Methods, consider reading a few tutorials, like this one from W3Schools: https://www.w3schools.com/tags/ref_httpmethods.asp.

#### Examining the Flask template (optional)
If you want to take a deeper dive into the flask template, then look through the [Exploring the Template](day-7-flask-extensions.md#exploring-the-template) section of the Flask resources. This is helpful to know, but honestly not always helpful when students are building their first MVC project - less is often more the first time around, and that we can dig deeper later if we need to.

#### Takeaways

* MVC - Explain the basic structure of an MVC application
* MVC - Use the 'restaurant' example of MVC to describe the different functions of the Model, View and Controller
* MVC - Explain "separation of concerns" and why it guides our designs

## HTTP GET Method

HTTP stands for Hypertext Transfer Protocol. We're not going to cover it all. Instead, we're going to cover the two **methods** (yes methods - just like Python uses methods to execute certain actions, the entire web is built on its own set of actions) used most commonly, and the only two that will be widely used in the scope of apps we build in this course.

A `GET` request is exactly what it sounds like. You tell your browser to GET information from a certain web address (a certain URL), and the browser goes and gets the information stored at that address. While that sounds simple, there's actually a lot of behind the scenes processing of information that happens, most of which is beyond the scope of this course.

The key thing to understand here is that when you type https://www.upperlinecode.com/, the server hosting that site has specific instructions for what to send you (the HTML code of the homepage, usually called index.html). The same is true if you were to type https://www.upperlinecode.com/p5 - the server hosting that page has specific instructions for what to send back (the HTML code for a page where you can sign up to host an Upperline Workshop, probably in a file called host-a-workshop.html or something similar).

## Routes

So now that we understand the idea of a `GET` request, we should write some of our own.

Have students add the following code to `routes.py`:
```python
@app.route('/secret')
def secret():
    return "<h1>You found the secret!</h1>"
```

Now ask them to figure out what they would need to type to make the 'you found the secret' text appear.

#### Playtime
* Have students code and test out 2-5 additional routes.

## Templates

That's lovely, but as you can tell, typing an entire HTML page in a single string probably doesn't seem quite right. That's why we use templates!

We're going to make two changes to our code:
1. At the very first line of our routes.py document, let's import the method we'll use to render templates:
```Python
from flask import render_template
```

2. In our index route, change the return value from a string to this method:
```python
def index():
    return render_template('index.html')
```

Notice that now, when we use one of our index routes (`/` or `/index`), we get the entire index.html page back!

#### Jinja3

We can personalize the landing page based on information from the user. We'll need to modify both the route and the template.  

Let's pass two additional pieces of information to the `render_template` function: a `title` string, and a `user` JSON object.
```python
def index():
    user = {'name': 'Alejandra'}
    return render_template('index.html', title='Home', user=user)
```

Let's modify the template so that it fills in information about the user and the title.
```html
<html>
    <head>
      <title>{{ title }} - Microblog</title>
    </head>
    <body>
        <h1>Hello, {{ user.name }}!</h1>
    </body>
</html>
```

The double curly braces (sometimes called moustache brackets) are used to fill in the blank with data that was passed in as arguments of the render_template method.

#### Playtime
Have students build out a `resultspage.html`, a route that takes you there, and at least one piece of information that is rendered through templating (the moustache brackets).

## Forms

This is great, but all of our information is still coming from the routing document, and we need some of it to be able to come from our users, so we're going to need to add a form. Here's a simple one:
```html
<form method="post" action="/sendBreakfast">
  <label for="nickname">What's your nickname?</label>
  <input type='text' name='nickname'>
  <label for="breakfast">What did you have for breakfast?</label>
  <input type='text' name='breakfast'>
  <input type='submit'>
</form>
```

If you try to use that form, you'll notice that it throws an error, and that's because we haven't written a route for `/sendBreakfast` yet.

add this to your routes document:
```python
@app.route('/sendBreakfast')
def handleBreakfast():
    return "Breakfast should appear here"
```

If you try submitting your form, you'll notice that you can a new error: `Method not allowed`. Interestingly, you'll also notice that if you reload the page, you'll see the "Breakfast should appear here" message does indeed appear. In other words, it's accessible from a GET method (when you just try to load the page), but not from a POST method (when you try to send info via a form).

Refactoring this so that it works for BOTH HTTP methods is actually pretty straightforward. Just add a methods list as one of the arguments:
```python
@app.route('/sendBreakfast', methods=['GET', 'POST'])
def handleBreakfast():
    return "Breakfast should appear here"
```

## HTTP POST Method
If the GET method is how you *ask* for information like specific webpages, the POST method is how you *send* information.

Consult the [flask extensions guide](day-7-flask-extensions.md#http-post-method) for a more detailed explanation of how and why the POST method exists.

In order for us to deal with both GET and POST requests, we need to add a few more parts of Flask to our application. First, let's import the part of Flask that allows us to interact with GET and POST requests more specifically.
```Python
from flask import render_template
from flask import request
```

Now that we have access to the requests that are used, we can start responding to each on in slightly different ways.

```python
@app.route('/sendBreakfast', methods=['GET', 'POST'])
def handleBreakfast():
    if request.method == 'GET':
        return "You're getting the breakfast page!"
    else:
        return "You're posting to the breakfast page"
```

Test this out with students. They'll notice that using the form to send a breakfast will access the "posting" result, but refreshing the page or typing the URL from scratch will access the "getting" result.

Now's the fun part - we need to access the form data that actually got sent, so to do that, we'll store the form data in a dictionary and log it to the console. See the two lines added under the `else` below:
```python
@app.route('/sendBreakfast', methods=['GET', 'POST'])
def handleBreakfast():
    if request.method == 'GET':
        return "You're getting the breakfast page!"
    else:
        userdata = dict(request.form)
        print(userdata)
        return "You're posting to the breakfast page"
```

Test this with students, and they'll notice that the dictionary printed has keys that look familiar. Ask them where those key names come from. They will sleuth out that those are the input 'name' attributes from the form.

Important note: the values in the key-value pairs coming from the form are in list form, so you'll need to use the index of 0 to access the first item in the list, rather than the using list itself.

So to access individual values is pretty simple. Concatenate those into a more dynamic string:
```python
# Store the nickname in a variable for easy reference
nickname = userdata['nickname'][0] # Note that we access the first item in the list provided by the "nickname key"
# Store the breakfast in a variable for easy reference
breakfast = userdata['breakfast'][0]
# Use those variables to create a dynamic result for our user
return "Hello, " + nickname + "! I hear you had " + breakfast + " for breakfast! Sounds delicious."
```

> Fun error: I accidentally returned `"I hear you had JEFF for breakfast! Sounds delicious."` the first time and in addition to be being supremely silly, the opportunity to debug things like that is actually golden, so if something like that happens, don't fret. Just dig into it with students.

Ask students:
* Do our variable names have to be the same as our dictionary keys? If not, why did we choose to reuse those names?
* Right now we're returning a String - we could start to include HTML elements in this string, or we could render a template. Which would be the better choice for our project? Why?
* What happens if we give two inputs in our form the same 'name' attribute? How would this affect the dictionary that is passed in our POST request?

## Models

The last thing we need is to be able to manipulate our user's input in some way. Have students name where they use forms on the internet. Some exemplary answers:
* Logging in to websites
* Searching (for flights, for airBNBs, for restaurants)
* Ordering / buying
* Online quizzes

All of those forms ultimately have the same job: take the info you provide, process that data in some way, and then return results to the user.

For example, if all we took from our users were their nickname and breakfast, we could build a ton of crazy apps with that information.
* We could build a name-rater system that tells them how cool their name is.
* We could build a word-scrambler that scrambles the letters in their name.
* We could build a breakfast-analyzer that tells how nutritious the user's breakfast was.
* We could build a secret breakfast guesser that congratulates the user if they had a special breakfast.

All of that assumes that we only ask for breakfast and name, but we can ask for so much other information by modifying our form later. For now, though, we just need to know how to hook up our back-end logic to our flask app.

Here's what needs to happen:
1. Write a model (usually a function or an object) in our models folder.
2. Import that model into our routes.py document.
3. Use that model to modify our user data before rendering the template.

#### Write the model

In the models folder, there is a model.py file.

Inside that model, let's write a shout function:
```python
def shout(word):
    return word.upper() + "!!"
```

> Some students might point out that there's no reason to make an entire model for this. Since it's just one line of code, we could just WRITE that one line of code instead. While that's true now, it'll become significantly less true as the model gets more complicated.

#### Import the model

At the top of our routes document, add another import line. At this point, we should have four:
```Python
from flask import render_template
from flask import request
from app import app
from app.models import model
```

> The only part that's a little confusing about this is that the assumed root directory of these import statements is the root of your entire flask project, so the path to import your models (as long as they are written in the models folder will always be app.models. We've used the filename `model.py` but students will likely find it helpful when they write their own models to create more precisely named models.

Test this to see if the import statement ran without error. Flask is very quick to let you know when your import statements do not work.

#### Use the model

Just like in all our labs before now, we'll use `filename.function()` to run the function we wrote in a separate file. In this case, that will be `model.shout('some string here')`.

In context, we'll be using our model to mutate the strings we get from our userdata before we store them in the variables we're using.

```python
userdata = dict(request.form)
nickname = model.shout(userdata['nickname'])
breakfast = model.shout(userdata['breakfast'])
return "Hello, " + nickname + "! I hear you had " + breakfast + " for breakfast! Sounds delicious."
```

## Next steps:
* Create a `results.html` template that uses the name and breakfast values in the context of a larger HTML page.
* Write a model that does something more interesting.
* Modify the form so that it takes other inputs like how many servings they had.
* Add [images and style](day-7-flask-extensions.md#static-resources) to the results page.
  * Bonus points if the images are dependent upon what breakfast the user entered.
* Add multiple templates and route to different ones depending on the user's answer.
