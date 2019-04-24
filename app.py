from flask import Flask, redirect, request, render_template, session, url_for
import db
import api
app = Flask(__name__)
app.secret_key = 'foobar'

@app.route('/')
def index():
    return render_template('index.html', session=session)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for("portfolio"))
    if request.method == 'POST':
        auth_ok= db.authenticate_user(
                    request.form['email'],
                    request.form['password'])
        if auth_ok:
            session['email'] = request.form['email']
            return redirect('/portfolio')
        else:
            return redirect("/login")
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'email' in session:
        return redirect(url_for("portfolio"))
    if request.method == 'POST':
        created_ok = db.create_user(
                    request.form['name'],
                    request.form['email'],
                    request.form['password'])
        if created_ok:
            return redirect("/login")
        else:
            return redirect("/register")
    else:
        return render_template('register.html')

@app.route('/logout', methods=['GET'])
def logout():
	if 'email' in session:
		session.pop('email')
	return redirect(url_for('index'))

@app.route('/portfolio')
def portfolio():
    if 'email' not in session:
        return redirect(url_for("index"))
    user_cash = db.get_user_cash(session['email'])
    user_holdings = db.get_user_holdings(session['email'])
    holdings_prices = api.batch_get_info([holding['ticker'] for holding in user_holdings], ['price'])
    user_portfolio = [(holding['ticker'], holding['quantity'], holdings_prices[holding['ticker']][price]*holding['quantity']) for holding in user_holdings]
    user_portfolio_value = sum([user_portfolio_item[2] for user_portfolio_item in user_portfolio])
    return render_template('portfolio.html', session=session)

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if 'email' not in session:
        return redirect(url_for("index"))
    if request.method == 'POST':
        price = api.get_price(request.form['ticker'])
        if price == 'Unknown symbol':
            # error
            pass
        else:
            total_price = float(price) * int(request.form['quantity'])
            user_cash = db.get_user_cash(session['email'])
            if total_price <= user_cash:
                # update available cash
                # add transaction
                # add holding
                pass
            else:
                # error
                pass
        return redirect(url_for("portfolio"))

    return redirect(url_for('index'))
