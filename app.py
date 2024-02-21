import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///reservation.db")

def get_class_schedule():
    conn = sqlite3.connect('reservation.db')
    conn.row_factory = sqlite3.Row
    classes = conn.execute('SELECT * FROM classes ORDER BY day').fetchall()
    conn.close()
    return classes

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        # Add validation for first name and last name
        if not first_name:
            return apology("must provide first name", 400)
        if not last_name:
            return apology("must provide last name", 400)

        if not username:
            return apology("must provide username", 400)
        elif not password:
            return apology("must provide password", 400)

        # Ensure confirmation was submitted and matches password
        elif not confirmation or password != confirmation:
            return apology("passwords do not match", 400)

        # Check if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0:
            return apology("username already exists", 400)

        # Hash password
        hash = generate_password_hash(password)

        # Insert the new user into users table
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        # Redirect to login page
        return redirect("/login")
    else:
        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("register.html")


@app.route("/about", methods=["GET"])
def about():
    """Render the about the studio page"""
    return render_template("about.html")


@app.route("/gallery", methods=["GET"])
def gallery():
    """Render the gallery page"""
    images = [
        {"url": "static/portfolio/WechatIMG24752.jpg", "alt": "Image 1 Description"},
        {"url": "static/portfolio/WechatIMG24753.jpg", "alt": "Image 2 Description"},
        {"url": "static/portfolio/WechatIMG24754.jpg", "alt": "Image 3 Description"},
        {"url": "static/portfolio/WechatIMG24755.jpg", "alt": "Image 4 Description"},
        {"url": "static/portfolio/WechatIMG24756.jpg", "alt": "Image 5 Description"},
        {"url": "static/portfolio/WechatIMG24757.jpg", "alt": "Image 6 Description"},
        {"url": "static/portfolio/WechatIMG24758.jpg", "alt": "Image 7 Description"},
        {"url": "static/portfolio/WechatIMG24759.jpg", "alt": "Image 8 Description"},
        {"url": "static/portfolio/WechatIMG24760.jpg", "alt": "Image 9 Description"},
        {"url": "static/portfolio/WechatIMG24761.jpg", "alt": "Image 10 Description"},
        # Add more images as needed
    ]
    return render_template('gallery.html', images=images)


@app.route("/contact")
def contact():
    """Render the contact page"""
    return render_template('contact.html')


@app.route("/make_reservation", methods=["GET", "POST"])
@login_required  # Ensures only logged-in users can make a reservation
def make_reservation():
    if request.method == "POST":
        # Retrieve form data
        class_id = request.form.get("class_id")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        user_id = session["user_id"]  # Get the logged-in user's ID
        print(user_id, class_id, first_name, last_name, email)  # Debugging
        # Insert reservation into the database
        db.execute("INSERT INTO reservations (user_id, class_id, first_name, last_name, email) VALUES (?, ?, ?, ?, ?)",
                   user_id, class_id, first_name, last_name, email)
        #debugged: python sees placeholder value (user_id,...) as a single value, removed parathesis, bug resolved

        flash("Reservation successful!")
        return redirect(url_for('make_reservation'))

    class_schedule = get_class_schedule()
    return render_template("make_reservation.html", class_schedule=class_schedule)


@app.route("/manage_reservation", methods=["GET"])
@login_required
def manage_reservation():
    user_id = session["user_id"]
    user_reservations = db.execute("SELECT * FROM reservations JOIN classes ON reservations.class_id = classes.id WHERE user_id = ?", (user_id,))
    return render_template("manage_reservation.html", reservations=user_reservations)


@app.route("/cancel_reservation/<int:reservation_id>", methods=["POST"])
@login_required
def cancel_reservation(reservation_id):
    user_id = session["user_id"]

    # Verify that the reservation belongs to the logged-in user
    reservation = db.execute("SELECT * FROM reservations WHERE id = ? AND user_id = ?", reservation_id, user_id)
    if reservation:
        # Check if the reservation exists in the list of results
        if any(reservation["id"] == reservation_id for reservation in reservation):
            db.execute("DELETE FROM reservations WHERE id = ? AND user_id = ?", reservation_id, user_id)
            flash("Reservation cancelled successfully.")
        else:
            flash("Reservation does not belong to you.", "error")
    else:
        flash("Reservation could not be found.", "error")

    return redirect(url_for('manage_reservation'))


