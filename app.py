from flask import Flask, flash, jsonify, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
# from flask_session import Session
from helpers import location
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

@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    q = request.args.get("q")
    rows = db.execute("SELECT * FROM users WHERE username = :username", username= q)
    # print(rows)
    # print(q)
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
            return render_template ('register.html',  message = "You must provide a username")
        #check password
        elif not password:
            return render_template('register.html', message = "Password not provided")
        #check if passwords match
        elif password != confirmation:
           return render_template('register.html',  message = "Passwords do no match")

        #confirm username has not been taken
        elif (rows):
            return render_template('register.html', message = "Username has been taken")
        #With all conditions met Insert user into database
        else:
            db.execute("INSERT INTO users(first, last, username, phone, email, password, address,  state, city,  gender) VALUES(:first, :last, :username, :phone, :email, :password, :address,  :state, :city,  :gender)", 
            first = first, last = last, username =username, phone=phone, email=email,  password = generate_password_hash(password), address = address,  state=state,  city = city, gender = gender)

            rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)

            # Remember which user has logged in
            # session["user_id"] = rows[0]["id"]
            return render_template("profile.html", message ="You have successfully registered")

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

