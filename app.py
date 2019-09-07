import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Mail, Message
# from flask_session import Session
from helpers import location
from cs50 import SQL
from helpers import naira, login_required
import datetime
from dateutil.relativedelta import relativedelta




app = Flask(__name__)

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] =  False
# app.config["MAIL_DEBUG"] = True`
app.config["MAIL_USERNAME"] = 'darotudeen@gmail.com'
app.config["MAIL_PASSWORD"] =  'Youngster1'
app.config["MAIL_DEFAULT_SENDER"] = 'darotudeen@gmail.com'
app.config["MAIL_MAX_EMAILS"] = None
# app.config["MAIL_SUPPRESS_SEND"] = False
app.config["MAIL_ASCII_ATTACHMENTS"] = False

mail = Mail(app)

# app.config['SESSION_TYPE'] = 'memcached'
app.secret_key = os.urandom(24)
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
     # Forget any user_id
    session.clear()

    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():

    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template('login.html', message_error = "must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template('login.html', message_error= "must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return render_template('login.html', message_error = "invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # print("MEEEE")
        # print(session["user_id"])
        

        # Redirect user to home page
        userDetails = db.execute('SELECT * FROM users WHERE id = :userId', userId= session["user_id"])
        return render_template("profile.html", message = "You have successfully logged in", userName=userDetails[0]["username"])
        

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    return render_template("login.html")

@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    q = request.args.get("q")
    rows = db.execute("SELECT * FROM users WHERE username = :username", username= q)
    if (rows):
        return jsonify(message = "True")
    return jsonify(message = "False")

@app.route('/register', methods=["GET", "POST"]) 
def register():
    # render page on get request
    if request.method == 'GET':
        response = location()
        return render_template("register.html",  message_get = response)
    elif request.method == 'POST':
        first = request.form.get('firstname')
        last = request.form.get('lastname')
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        gender = request.form.get('gender')
        address = request.form.get('address')
        state = request.form.get('state')
        city = request.form.get('city')
                # check for existing username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        #check username
        if not username:
                return render_template ('register.html',  message = [" ", "You must provide a username"])
            #check password
        elif not password:
                return render_template('register.html', message = [" ", "Password not provided"])
            #check if passwords match
        elif password != confirmation:
                return render_template('register.html',  message = [" ", "Passwords do no match"])

            #confirm username has not been taken
        elif (rows):
                return render_template('register.html', message = [" ", "Username has been taken"])
        #With all conditions met Insert user into database
        else:
            db.execute("INSERT INTO users(first, last, username, phone, email, password, address,  state, city,  gender) VALUES(:first, :last, :username, :phone, :email, :password, :address,  :state, :city,  :gender)", 
            first = first, last = last, username =username, phone=phone, email=email,  password = generate_password_hash(password), address = address,  state=state,  city = city, gender = gender)

            rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)
            msg = Message("You have successfully registered on Decapay", recipients=[email])

            userDetails = db.execute('SELECT * FROM users WHERE id = :userId', userId= session["user_id"])
            return render_template("profile.html",message ="You have successfully registered", userName=userDetails[0]["username"])   
            

@app.route('/create', methods=["GET", "POST"])
@login_required
def create():    
    if session.get("user_id") is None:
        return render_template("notfound.html", details="Login Is Required")
    elif request.method =="POST":
                startdate = datetime.datetime.now()
                loantype = request.form.get("loantype")               
                amountborrowed = int(request.form.get("amountborrowed"))
                interestRate = float(request.form.get("interestrate"))
                period = int(request.form.get("period"))
                totalInterest = amountborrowed * interestRate
                totalCostOfLoan = amountborrowed + totalInterest
                monthlyPayment = totalCostOfLoan / period
                monthlyInterest = totalInterest / period
                monthlyPrincipal = monthlyPayment - monthlyInterest  
               
                # insert loan details into loan table             
                k = db.execute("INSERT INTO loans (userId, loanType, loanAmount, interestRate, loanPeriod, monthlyRepayment, totalInterest,  totalCostOfLoan, startdate) VALUES(:userId, :loanType, :loanAmount, :interestRate, :loanPeriod, :monthlyRepayment, :totalInterest,  :totalCostOfLoan, :startdate)",
                userId= session["user_id"], loanType = loantype, loanAmount = naira(amountborrowed), interestRate = interestRate, loanPeriod = period, monthlyRepayment = monthlyPayment, totalInterest = naira(totalInterest),  totalCostOfLoan= totalCostOfLoan, startdate = startdate) 
                return render_template("/success.html")
    elif request.method=="GET":
        userLoans = db.execute('SELECT * FROM loans WHERE userId = :userId', userId= session["user_id"])
        # print(userLoans)
        if not userLoans:
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
                    userDetails = db.execute('SELECT * FROM users WHERE id = :userId', userId= session["user_id"])
                    return render_template("profile.html",message ="You have successfully registered", userName=userDetails[0]["username"])   
        else:
            return render_template("noteligible.html", details="Please Pay up before making another application")       

@app.route('/history')
@login_required
def history():
    userLoans = db.execute('SELECT * FROM loans WHERE userId = :userId', userId= session["user_id"])
    payment = naira(float(userLoans[0]["monthlyRepayment"]))
    tbalance = naira(userLoans[0]["totalCostOfLoan"])
    # print(userLoans)

    return render_template("paymenthistory.html",userLoans = userLoans,payment = payment, tbalance =tbalance)

@app.route('/duepayment')
@login_required
def duepayment():
    if request.method == "GET":
        startdate = datetime.datetime.now()
        userLoans = db.execute('SELECT * FROM loans WHERE userId = :userId', userId= session["user_id"])
        date = (startdate + relativedelta(months=+1)).strftime("%x")
        period = userLoans[0]["loanPeriod"]
        userLoans[0]["totalInterest"]
        payment = float(userLoans[0]["monthlyRepayment"])
        rate = userLoans[0]["interestRate"]
        tbalance = userLoans[0]["totalCostOfLoan"]
        print(tbalance)
        balances = []
        dates =[]
        print(period)
        print(payment)
        for x in range(period):
            date = (startdate + relativedelta(months=+x)).strftime("%x")
            balance = tbalance - (x * payment)
            balance = naira(balance)
            balances.append(balance)
            dates.append(date)
        return render_template("duepayment.html",userLoans = userLoans, dates = dates,balances = balances,period = period)

@app.route('/success')
def success():
    return render_template("success.html")

@app.route('/profile')
@login_required
def profile():
    if session.get("user_id") is None:
        return render_template("notfound.html", details="Login Is Required")
    else:
        userDetails = db.execute('SELECT * FROM users WHERE id = :userId', userId= session["user_id"])
        return render_template("profile.html", userName=userDetails[0]["username"])

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    flash('You have successfully logged out')
    # Redirect user to login form
    return redirect("/login")


