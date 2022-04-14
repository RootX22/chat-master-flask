import os
from datetime import datetime
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask (__name__)
app.secret_key = os.getenv("SECRET", "randomstring123")  
""" Secret key changed to an environment variable. Helps generate session ID """
messages = []

def add_message(username, message):
    """ Add messages to the 'messages' list """
    """ 1st set of {} refers to 1st argument = username """
    """ 2nd set of {} refers to 2nd argument = message """
    """ Python can accept either {1} or {} """
    now = datetime.now().strftime("%H:%M:%S") # new variable = now
    
    messages.append({"timestamp": now, "from": username, "message":message})

@app.route('/', methods = ["GET", "POST"]) # route decorator that aligns to index.html
def index():
    """ Main page with instructions """
    if request.method == "POST":
        session["username"] = request.form["username"]
        
    if "username" in session:
        return redirect(url_for("user", username=session["username"]))
    
    return render_template("index.html") # 'index.html' now replaces message

@app.route('/chat/<username>', methods = ["GET", "POST"])
def user(username):
    """ Add & Display chat messages. {0} = username argument """
    """ username & messages get added to the list """
    if request.method == "POST":
        username = session["username"]
        message = request.form["message"]
        add_message(username,message)
        return redirect(url_for("user", username=session["username"]))
    
    return render_template("chat.html", username = username, chat_messages = messages)
    
app.run(host=os.getenv('IP', "0.0.0.0"), port=int(os.getenv('PORT', "5000")), debug=False) # debug=False for production. 
""" Fallback values for IP = 0.0.0.0 & PORT = 5000 """

