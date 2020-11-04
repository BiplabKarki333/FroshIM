from flask import Flask, request, render_template, redirect
import sqlite3
from flask_mail import Mail, Message
import os

SPORTS = ['Soccer', 'Volleyball', "Table_tennis"]

conn = sqlite3.connect('registrants.db', check_same_thread = False)
c = conn.cursor()

c.execute('''CREATE TABLE registrants (email text, sport text)''')



app = Flask(__name__)
app.config["MAIL_DEFAULT_SENDER"] = 'karkibiplab62@gmail.com'
app.config["MAIL_PASSWORD"] = "CarlSagan333!"
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "karkibiplab62@gmail.com"
mail = Mail(app)


@app.route("/")
def index():
    return render_template('index.html', sports = SPORTS)

@app.route("/register", methods = ["POST"])
def register():
    email = request.form.get('email')
    sports = request.form.get('sports')

    if not email:
        return render_template('failure.html', message = "Did you forget to enter your name?")
    if not sports:
        return render_template('failure.html', message = "Did you forget to choose a sport?")
    if sports not in SPORTS:
        return render_template('failure.html', message = "You are clever! But I caught you.")
    if email in REGISTRANTS.keys():
        return render_template('reregistration.html')

    c.execute("INSERT INTO registrants VALUES(?,?)",(email, sports))
    conn.commit()

    message = Message("You are registered!", recipients = [email])
    mail.send(message)
    return redirect('/registrants')

@app.route("/registrants", methods= ['GET',"POST"])
def registrants():
    registrants_list = c.execute("SELECT * FROM registrants")
    return render_template('registrants.html', registrants = registrants_list )
