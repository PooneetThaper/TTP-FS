from flask import Flask, redirect, request, render_template, session, url_for
from werkzeug import generate_password_hash, check_password_hash
import db
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for("portfolio"))
    if request.method == 'POST':
        print(request.form)
        # authenticate
        # session
        # redirect to portfolio
        return redirect("/login")
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'email' in session:
        return redirect(url_for("portfolio"))
    if request.method == 'POST':
        print(request.form)
        # db.create_user(
        #     request.form['name'],
        #     request.form['email'],
        #     request.form['password'])
        return redirect("/login")
    else:
        return render_template('register.html')

@app.route('/portfolio')
def portfolio():
    return render_template('index.html')

@app.route('/transactions')
def transactions():
    return render_template('index.html')
