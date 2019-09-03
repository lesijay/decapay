from flask import Flask, flash, jsonify, redirect, render_template, request, session
# from flask_session import Session
from cs50 import SQL

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///decapay.db")

@app.route('/')
def index():
    k = db.execute("SELECT * FROM users ")    
    print(k)
    print("joel test")
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/create')
def create():
    return render_template("create.html")
    
@app.route('/payment')
def payment():
    return render_template("duepayment.html")

# if __name__ == "__main__":
#     app.run()

