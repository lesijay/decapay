from flask import Flask, flash, jsonify, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
# from flask_session import Session
from helpers import location
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

@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    q = request.args.get("q")
    rows = db.execute("SELECT * FROM users WHERE username = :username", username= q)
    print(rows)
    print(q)
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
            return render_template("register.html", message ="You have successfully registered")

@app.route('/create')
def create():
    return render_template("create.html")
    
@app.route('/payment')
def payment():
    return render_template("duepayment.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

# if __name__ == "__main__":
#     app.run()

