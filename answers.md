# Answers / Code Snippets

Howdy folks! This top-secret markdown file exists to save you some typing time.

Here's the code used for a "new event" form in video 4.

```html
<!DOCTYPE html>
<html>
    <head>
        <title>Community Events Board</title>
    </head>
    <body>
        <h1>Community Events Board</h1>
        <form method="post" action="/events/new">
            <label for="event_name">Event Name:</label>
            <input type="text" name="event_name" value=""/>
            <label for="event_date">Date:</label>
            <input type="date" name="event_date" value=""/>
            <label for="user_name">Name:</label>
            <input type="text" name="user_name" value=""/>
            <input type="submit" value="Submit"/>
        </form>
    </body>
</html>
```
