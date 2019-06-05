from flask import Flask, redirect, request, render_template, session, url_for
import db
import api
app = Flask(__name__)
app.secret_key = 'foobar'

def buy_ticker(email, ticker, quantity):
    price = api.get_price(request.form['ticker']).json()
    if price == 'Unknown symbol':
        # error
        return False
    else:
        total_price = price * quantity
        user_cash = db.get_user_cash(session['email'])
        if total_price <= user_cash:
            db.update_user_cash(session['email'], user_cash - total_price)
            db.create_transaction(session['email'], 'buy', ticker, quantity, total_price)
            db.update_holding(session['email'], ticker, quantity)
            return True
        else:
            # error
            return False

def sell_ticker(email, ticker, quantity):
    price = api.get_price(request.form['ticker']).json()
    if price == 'Unknown symbol':
        # error
        return False
    else:
        user_holding = db.get_user_holdings(session['email'], ticker)
        if user_holding == None:
            return False
        elif user_holding.quantity >= quantity:
            total_price = price * quantity
            user_cash = db.get_user_cash(session['email'])
            db.update_user_cash(session['email'], user_cash + total_price)
            db.create_transaction(session['email'], 'sell', ticker, quantity, total_price)
            db.update_holding(session['email'], ticker, quantity*-1)
            return True
        else:
            #error
            return False

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

def holding_color(price, open):
    if price == open:
        return 'grey'
    elif price < open:
        return 'red'
    else:
        return 'green'

@app.route('/portfolio')
def portfolio():
    if 'email' not in session:
        return redirect(url_for("index"))
    user_cash_amount = "%.2f" % db.get_user_cash(session['email'])
    user_holdings = db.get_user_holdings(session['email'])
    holdings_prices = api.batch_get_info([holding.ticker for holding in user_holdings], ['price','ohlc']).json()
    user_portfolio = [( holding.ticker,
                        holding.quantity,
                        holdings_prices[holding.ticker.upper()]['price']*holding.quantity,
                        holding_color(  holdings_prices[holding.ticker.upper()]['price'],
                                        holdings_prices[holding.ticker.upper()]['ohlc']['open']['price']))
                        for holding in user_holdings]
    user_portfolio_value = sum([user_portfolio_item[2] for user_portfolio_item in user_portfolio])
    return render_template('portfolio.html', session=session, user_portfolio=user_portfolio, user_portfolio_value=user_portfolio_value, user_cash_amount=user_cash_amount)

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    print(request.form)
    if 'email' not in session:
        return redirect(url_for("index"))
    if request.method == 'POST':
        if request.form['type'] == 'buy':
            buy_ticker(session['email'], request.form['ticker'], int(request.form['quantity']))
        else:
            sell_ticker(session['email'], request.form['ticker'], int(request.form['quantity']))
        return redirect(url_for("portfolio"))
    user_cash_amount = "%.2f" % db.get_user_cash(session['email'])
    user_transactions = [(transaction.date_time[:-10], transaction.type, transaction.ticker, transaction.quantity, transaction.amount) for transaction in db.get_user_transactions(session['email'])]
    return render_template('transaction.html', session=session, user_transactions=user_transactions, user_cash_amount=user_cash_amount)
