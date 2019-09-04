from flask import Flask, flash, jsonify, redirect, render_template, request, session
# from flask_session import Session
from cs50 import SQL
from helpers import naira

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
    # k = db.execute("SELECT * FROM users ")    
    # print(k)
    print("joel test")
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/create', methods=["GET", "POST"])
def create():
        if request.method =="POST":
                loantype = request.form.get("loantype")               
                amountborrowed = request.form.get("amountborrowed")
                interestRate = request.form.get("interestrate")
                period = request.form.get("period")
                print(loantype, amountborrowed, interestRate,period)
                return render_template("/success.html")
        if request.method=="GET":
                loantype = request.args.get("loantype")        
                if loantype == "Decamini":
                        interestRate = 0.03
                        return render_template("create.html",loantype=loantype, mini=100000, max=300000, interestRate=interestRate)
                elif loantype == "Decaflex":
                        interestRate = 0.05
                        return render_template("create.html",loantype=loantype, mini=310000, max=900000, interestRate=interestRate)
                elif loantype == "Decalarge":
                        interestRate = 0.10
                        return render_template("create.html",loantype=loantype, mini=910000, max=2000000, interestRate=interestRate)
                else:
                        return render_template("/profile.html")

@app.route('/payment')
def payment():
    return render_template("duepayment.html")

@app.route('/duepayment')
def duepayment():
    return render_template("duepayment.html")

@app.route('/success')
def success():
    return render_template("success.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

# if __name__ == "__main__":
#     app.run()

